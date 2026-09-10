from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Zone, DeviceProductCatalog, InstalledDevice


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "organization",
    )

    search_fields = (
        "name",
        "organization__legal_name",
    )

    list_filter = (
        "organization",
    )

    ordering = (
        "name",
    )

    list_select_related = (
        "organization",
    )


@admin.register(DeviceProductCatalog)
class DeviceProductCatalogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "manufacturer",
        "model_name",
        "sku",
    )

    search_fields = (
        "manufacturer",
        "model_name",
        "sku",
    )

    ordering = (
        "manufacturer",
        "model_name",
    )


@admin.register(InstalledDevice)
class InstalledDeviceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "internal_name",
        "product",
        "organization",
        "zone",
        "reference_power",
        "status",
    )

    search_fields = (
        "internal_name",
        "serial_number",
        "product__manufacturer",
        "product__model_name",
        "organization__legal_name",
        "zone__name",
    )

    list_filter = (
        "status",
        "organization",
        "zone",
    )

    ordering = (
        "internal_name",
    )

    list_select_related = (
        "product",
        "organization",
        "zone",
    )