from django import forms


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
        widget=forms.Textarea(attrs={
            "rows": 14,
            "placeholder": "Paste the full text of your CV here...",
            "class": "form-textarea",
        }),
    )

    def clean_job_offer(self):
        value = self.cleaned_data["job_offer"].strip()
        if len(value) < 50:
            raise forms.ValidationError("The job offer seems too short. Please paste the full text.")
        return value

    def clean_cv_text(self):
        value = self.cleaned_data["cv_text"].strip()
        if len(value) < 100:
            raise forms.ValidationError("The CV seems too short. Please paste the full text.")
        return value
