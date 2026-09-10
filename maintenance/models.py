from django.db import models

# Create your models here.
from django.db import models
from core.models import BaseModel
from accounts.models import  Organization
from devices.models import InstalledDevice

class MaintenanceRequest(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    device = models.ForeignKey(InstalledDevice, on_delete=models.PROTECT)
    reason = models.TextField()
    priority = models.CharField(max_length=20, default='medium') # low, medium, high
    status = models.CharField(max_length=20, default='pending') # pending, in_progress, closed
    assigned_to = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    actual_completion_date = models.DateTimeField(null=True, blank=True)
    diagnosis_notes = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Mantenimiento {self.device.internal_name} - {self.status}"