from django.db import models
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