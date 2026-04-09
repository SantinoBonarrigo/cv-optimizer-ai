from django.contrib import admin
from .models import AnalysisResult


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ("id", "match_score", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("job_offer", "cv_text", "match_score", "missing_keywords", "suggestions", "created_at")
    ordering = ("-created_at",)
