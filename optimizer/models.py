from django.db import models


class AnalysisResult(models.Model):
    job_offer = models.TextField(verbose_name="Job Offer")
    cv_text = models.TextField(verbose_name="CV Text")
    match_score = models.IntegerField(verbose_name="Match Score (0-100)")
    missing_keywords = models.JSONField(verbose_name="Missing Keywords")
    suggestions = models.JSONField(verbose_name="Improvement Suggestions")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Analysis Date")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Analysis Result"
        verbose_name_plural = "Analysis Results"

    def __str__(self):
        return f"Analysis #{self.pk} — Score: {self.match_score}/100 ({self.created_at.strftime('%d/%m/%Y %H:%M')})"
