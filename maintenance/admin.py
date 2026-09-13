from django.contrib import admin

from accounts.models import Organization, UserProfile
from devices.models import InstalledDevice
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        try:
            organization = request.user.profile.organization
        except UserProfile.DoesNotExist:
            return qs.none()

        return qs.filter(organization=organization)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            try:
                organization = request.user.profile.organization

                if db_field.name == "organization":
                    kwargs["queryset"] = Organization.objects.filter(
                        id=organization.id
                    )

                if db_field.name == "device":
                    kwargs["queryset"] = InstalledDevice.objects.filter(
                        organization=organization
                    )

            except UserProfile.DoesNotExist:
                if db_field.name == "organization":
                    kwargs["queryset"] = Organization.objects.none()

                if db_field.name == "device":
                    kwargs["queryset"] = InstalledDevice.objects.none()

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            try:
                obj.organization = request.user.profile.organization
            except UserProfile.DoesNotExist:
                return

        super().save_model(request, obj, form, change)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return (
                "priority",
                "status",
                "organization",
                "scheduled_date",
            )

        return (
            "priority",
            "status",
            "scheduled_date",
        )