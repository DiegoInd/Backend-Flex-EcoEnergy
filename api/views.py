
from django.utils import timezone
from rest_framework import viewsets

from .permissions import IsAPIAdminOrReadOnlyOperator

from accounts.models import Organization
from devices.models import Zone, DeviceProductCatalog, InstalledDevice
from maintenance.models import MaintenanceRequest
from monitoring.models import EnergyMeasurement
from .serializers import EnergyMeasurementSerializer

from .serializers import (
    OrganizationSerializer,
    ZoneSerializer,
    DeviceProductCatalogSerializer,
    InstalledDeviceSerializer,
    MaintenanceRequestSerializer,
)


# MODELO PRINCIPAL 1: ORGANIZACIONES
class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAPIAdminOrReadOnlyOperator]

    def get_queryset(self):
        return Organization.objects.filter(
            deleted_at__isnull=True
        ).order_by("id")

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


# MODELO PRINCIPAL 2: ZONAS
class ZoneViewSet(viewsets.ModelViewSet):
    serializer_class = ZoneSerializer
    permission_classes = [IsAPIAdminOrReadOnlyOperator]

    def get_queryset(self):
        return Zone.objects.filter(
            deleted_at__isnull=True
        ).order_by("id")

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


# MODELO PRINCIPAL 3: CATALOGO DE PRODUCTOS
class DeviceProductCatalogViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceProductCatalogSerializer
    permission_classes = [IsAPIAdminOrReadOnlyOperator]

    def get_queryset(self):
        return DeviceProductCatalog.objects.filter(
            deleted_at__isnull=True
        ).order_by("id")

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


# MODELO PRINCIPAL 4: DISPOSITIVOS INSTALADOS
class InstalledDeviceViewSet(viewsets.ModelViewSet):
    serializer_class = InstalledDeviceSerializer
    permission_classes = [IsAPIAdminOrReadOnlyOperator]

    def get_queryset(self):
        return InstalledDevice.objects.filter(
            deleted_at__isnull=True
        ).order_by("id")

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["deleted_at"])


# MODELO OPERACIONAL 1: SOLICITUDES DE MANTENIMIENTO
class MaintenanceRequestViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [IsAPIAdminOrReadOnlyOperator]

    def get_queryset(self):
        return MaintenanceRequest.objects.filter(
            deleted_at__isnull=True
        ).order_by("id")

class EnergyMeasurementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EnergyMeasurementSerializer
    permission_classes = [IsAPIAdminOrReadOnlyOperator]

    def get_queryset(self):
        return EnergyMeasurement.objects.filter(
            deleted_at__isnull=True
        ).order_by("id")
