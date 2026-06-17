from django.db import models


class BusinessPlan(models.Model):
    idea_text = models.TextField()
    plan_markdown = models.TextField(blank=True)
    detected_language = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Plan #{self.pk}: {self.idea_text[:50]}"
