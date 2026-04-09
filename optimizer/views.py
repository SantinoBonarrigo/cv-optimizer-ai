from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .forms import CVAnalysisForm
from .models import AnalysisResult
from .services import analyze_cv


def home(request):
    """
    GET  → renders the empty form.
    POST → analyzes the CV, saves to DB, and renders the result.
    """
    form = CVAnalysisForm()

    if request.method == "POST":
        form = CVAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                result_data = analyze_cv(
                    job_offer=form.cleaned_data["job_offer"],
                    cv_text=form.cleaned_data["cv_text"],
                )
                analysis = AnalysisResult.objects.create(
                    job_offer=form.cleaned_data["job_offer"],
                    cv_text=form.cleaned_data["cv_text"],
                    match_score=result_data["match_score"],
                    job_fit=result_data["job_fit"],
                    recommendation=result_data["recommendation"],
                    explanation=result_data["explanation"],
                    missing_keywords=result_data["missing_keywords"],
                    suggestions=result_data["suggestions"],
                    ats_friendly=result_data["ats_friendly"],
                    ats_issues=result_data["ats_issues"],
                    ats_tips=result_data["ats_tips"],
                )
                return render(request, "optimizer/result.html", {"analysis": analysis})
            except Exception as e:
                messages.error(request, f"Error analyzing CV: {e}")

    return render(request, "optimizer/home.html", {"form": form})


def history(request):
    """Displays all past analyses saved in the database."""
    analyses = AnalysisResult.objects.all()
    return render(request, "optimizer/history.html", {"analyses": analyses})


def detail(request, pk):
    """Displays the detail view for a specific historical analysis."""
    analysis = get_object_or_404(AnalysisResult, pk=pk)
    return render(request, "optimizer/result.html", {"analysis": analysis, "from_history": True})
