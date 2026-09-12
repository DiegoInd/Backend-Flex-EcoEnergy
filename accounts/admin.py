from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Organization, Department, UserProfile


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

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "organization",
        "department",
        "employee_code",
        "phone",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "employee_code",
    )

    list_filter = (
        "organization",
        "department",
    )

    list_select_related = (
        "user",
        "organization",
        "department",
    )