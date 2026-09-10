from django.db import models

# Create your models here.
from django.db import models
from core.models import BaseModel
from devices.models import InstalledDevice

class EnergyMeasurement(BaseModel):
    device = models.ForeignKey(InstalledDevice, on_delete=models.PROTECT)
    value = models.FloatField()
    unit = models.CharField(max_length=20, default='kWh')
    reading_timestamp = models.DateTimeField()
    source_type = models.CharField(max_length=20, default='manual') # manual o automatic
    # Si es manual, guardamos qué usuario la ingresó (usando el modelo User por defecto de Django)
    registered_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.device.internal_name} - {self.value} {self.unit} ({self.reading_timestamp})"