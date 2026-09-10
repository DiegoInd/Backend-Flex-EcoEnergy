from django.contrib import admin

# Register your models here.
from django.contrib import admin
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