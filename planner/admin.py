from django.contrib import admin
from .models import BusinessPlan

admin.site.site_header = "Business Plan Generator — Admin Console"
admin.site.site_title = "Business Plan Admin"
admin.site.index_title = "Manage Generated Plans"


@admin.register(BusinessPlan)
class BusinessPlanAdmin(admin.ModelAdmin):
    list_display = ("id", "short_idea", "detected_language", "created_at")
    search_fields = ("idea_text", "plan_markdown")
    readonly_fields = ("created_at",)

    @admin.display(description="Idea")
    def short_idea(self, obj):
        return obj.idea_text[:70]
