
from django.contrib import admin

from accounts.models import Organization, UserProfile
from .models import Zone, DeviceProductCatalog, InstalledDevice
from monitoring.models import EnergyMeasurement


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
        if db_field.name == "organization" and not request.user.is_superuser:
            try:
                organization = request.user.profile.organization
                kwargs["queryset"] = Organization.objects.filter(
                    id=organization.id
                )
            except UserProfile.DoesNotExist:
                kwargs["queryset"] = Organization.objects.none()

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


class EnergyMeasurementInline(admin.TabularInline):
    model = EnergyMeasurement
    extra = 0
    fields = (
        "value",
        "unit",
        "reading_timestamp",
        "source_type",
        "registered_by",
    )


@admin.register(InstalledDevice)
class InstalledDeviceAdmin(admin.ModelAdmin):

    inlines = (EnergyMeasurementInline,)
    actions = ("marcar_como_inactivo",)
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

                if db_field.name == "zone":
                    kwargs["queryset"] = Zone.objects.filter(
                        organization=organization
                    )

            except UserProfile.DoesNotExist:
                if db_field.name == "organization":
                    kwargs["queryset"] = Organization.objects.none()

                if db_field.name == "zone":
                    kwargs["queryset"] = Zone.objects.none()

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
                "status",
                "organization",
                "zone",
            )

        return (
            "status",
        )
    
    @admin.action(description="Marcar dispositivos seleccionados como inactivos")
    def marcar_como_inactivo(self, request, queryset):
        cantidad = queryset.update(status="inactive")

        self.message_user(
            request,
            f"{cantidad} dispositivo(s) marcado(s) como inactivo(s)."
        )