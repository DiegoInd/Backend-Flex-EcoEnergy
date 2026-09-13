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

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        try:
            organization = request.user.profile.organization
        except UserProfile.DoesNotExist:
            return qs.none()

        return qs.filter(id=organization.id)


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

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return (
                "is_active",
                "organization",
            )

        return (
            "is_active",
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

                if db_field.name == "department":
                    kwargs["queryset"] = Department.objects.filter(
                        organization=organization
                    )

            except UserProfile.DoesNotExist:
                if db_field.name == "organization":
                    kwargs["queryset"] = Organization.objects.none()

                if db_field.name == "department":
                    kwargs["queryset"] = Department.objects.none()

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
                "organization",
                "department",
            )

        return ()