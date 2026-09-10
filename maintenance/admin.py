from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import MaintenanceRequest


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device",
        "organization",
        "priority",
        "status",
        "assigned_to",
        "scheduled_date",
        "actual_completion_date",
        "cost",
    )

    search_fields = (
        "device__internal_name",
        "organization__legal_name",
        "assigned_to__username",
        "reason",
    )

    list_filter = (
        "priority",
        "status",
        "organization",
        "scheduled_date",
    )

    ordering = (
        "-created_at",
    )

    list_select_related = (
        "device",
        "organization",
        "assigned_to",
    )