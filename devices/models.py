from django.db import models

# Create your models here.
from django.db import models
from core.models import BaseModel
from accounts.models import Organization

class Zone(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.organization.legal_name})"

class DeviceProductCatalog(BaseModel):
    manufacturer = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, unique=True)
    specifications = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.manufacturer} - {self.model_name}"

class InstalledDevice(BaseModel):
    product = models.ForeignKey(DeviceProductCatalog, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    internal_name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    reference_power = models.FloatField()
    status = models.CharField(max_length=50, default='active')

    def __str__(self):
        return self.internal_name