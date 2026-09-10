from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Organization, Department


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "legal_name",
        "tax_identifier",
        "commercial_name",
        "is_active",
    )

    search_fields = (
        "legal_name",
        "tax_identifier",
        "commercial_name",
    )

    list_filter = (
        "is_active",
    )

    ordering = (
        "legal_name",
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "organization",
        "is_active",
    )

    search_fields = (
        "name",
        "organization__legal_name",
    )

    list_filter = (
        "is_active",
        "organization",
    )

    ordering = (
        "name",
    )

    list_select_related = (
        "organization",
    )