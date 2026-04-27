from django.contrib import admin

from .models import FaultReport


@admin.register(FaultReport)
class FaultReportAdmin(admin.ModelAdmin):
    list_display = (
        "tracking_code",
        "issue_type",
        "status",
        "is_hazard",
        "created_at",
    )
    list_filter = ("status", "issue_type", "is_hazard")
    search_fields = ("tracking_code", "description")
    readonly_fields = ("tracking_code", "created_at", "updated_at")
