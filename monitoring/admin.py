from django.contrib import admin

from accounts.models import UserProfile
from devices.models import InstalledDevice
from .models import EnergyMeasurement


@admin.register(EnergyMeasurement)
class EnergyMeasurementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device",
        "value",
        "unit",
        "reading_timestamp",
        "source_type",
        "registered_by",
    )

    search_fields = (
        "device__internal_name",
        "device__serial_number",
        "registered_by__username",
    )

    list_filter = (
        "unit",
        "source_type",
        "reading_timestamp",
    )

    ordering = (
        "-reading_timestamp",
    )

    list_select_related = (
        "device",
        "registered_by",
    )

    date_hierarchy = "reading_timestamp"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        try:
            organization = request.user.profile.organization
        except UserProfile.DoesNotExist:
            return qs.none()

        return qs.filter(device__organization=organization)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            try:
                organization = request.user.profile.organization

                if db_field.name == "device":
                    kwargs["queryset"] = InstalledDevice.objects.filter(
                        organization=organization
                    )

            except UserProfile.DoesNotExist:
                if db_field.name == "device":
                    kwargs["queryset"] = InstalledDevice.objects.none()

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )