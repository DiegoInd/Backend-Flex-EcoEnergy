from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from core.models import BaseModel


# PASO 4.A: Las tablas reales de organizaciones y departamentos
class Organization(BaseModel):
    legal_name = models.CharField(max_length=150)
    tax_identifier = models.CharField(max_length=50, unique=True)
    commercial_name = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.commercial_name or self.legal_name


class Department(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.organization.legal_name}"

class UserProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="user_profiles",
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="user_profiles",
        null=True,
        blank=True,
    )

    employee_code = models.CharField(
        max_length=30,
        unique=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    def clean(self):
        super().clean()

        if (
            self.department_id
            and self.department.organization_id
            != self.organization_id
        ):
            raise ValidationError({
                "department": (
                    "El departamento debe pertenecer "
                    "a la organización seleccionada."
                )
            })

    def __str__(self):
        return f"{self.user.username} - {self.organization}"