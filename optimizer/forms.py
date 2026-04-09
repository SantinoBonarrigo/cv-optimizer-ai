from django import forms
from .services import extract_pdf_text


class CVAnalysisForm(forms.Form):
    job_offer = forms.CharField(
        label="Job Offer",
        widget=forms.Textarea(attrs={
            "rows": 10,
            "placeholder": "Paste the full job description here...",
            "class": "form-textarea",
        }),
    )
    cv_text = forms.CharField(
        label="Your CV",
        required=False,
        widget=forms.Textarea(attrs={
            "rows": 10,
            "placeholder": "Paste the full text of your CV here...",
            "class": "form-textarea",
        }),
    )
    cv_pdf = forms.FileField(
        label="Or upload a PDF",
        required=False,
        widget=forms.FileInput(attrs={
            "accept": "application/pdf",
            "class": "form-file-input",
            "id": "cv_pdf",
        }),
    )

    def clean_job_offer(self):
        value = self.cleaned_data["job_offer"].strip()
        if len(value) < 50:
            raise forms.ValidationError("The job offer seems too short. Please paste the full text.")
        return value

    def clean_cv_pdf(self):
        pdf = self.cleaned_data.get("cv_pdf")
        if pdf:
            if not pdf.name.lower().endswith(".pdf") or pdf.content_type != "application/pdf":
                raise forms.ValidationError("Please upload a valid PDF file.")
            if pdf.size > 5 * 1024 * 1024:
                raise forms.ValidationError("PDF file must be under 5 MB.")
        return pdf

    def clean(self):
        cleaned_data = super().clean()
        pdf = cleaned_data.get("cv_pdf")
        cv_text = cleaned_data.get("cv_text", "").strip()

        if pdf:
            try:
                extracted = extract_pdf_text(pdf)
            except Exception as e:
                raise forms.ValidationError(f"Could not extract text from the PDF: {e}")
            if len(extracted.strip()) < 100:
                raise forms.ValidationError(
                    "The PDF appears to contain very little text. "
                    "Make sure it is not scanned/image-based."
                )
            cleaned_data["cv_text"] = extracted
        elif cv_text:
            if len(cv_text) < 100:
                raise forms.ValidationError("The CV seems too short. Please paste the full text.")
            cleaned_data["cv_text"] = cv_text
        else:
            raise forms.ValidationError("Please paste your CV text or upload a PDF.")

        return cleaned_data
