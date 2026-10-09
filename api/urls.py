
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    OrganizationViewSet,
    ZoneViewSet,
    DeviceProductCatalogViewSet,
    InstalledDeviceViewSet,
    MaintenanceRequestViewSet,
    EnergyMeasurementViewSet,
)

router = DefaultRouter()

router.register(
    "organizations",
    OrganizationViewSet,
    basename="organization",
)

router.register(
    "zones",
    ZoneViewSet,
    basename="zone",
)

router.register(
    "device-products",
    DeviceProductCatalogViewSet,
    basename="device-product",
)

router.register(
    "installed-devices",
    InstalledDeviceViewSet,
    basename="installed-device",
)

router.register(
    "maintenance-requests",
    MaintenanceRequestViewSet,
    basename="maintenance-request",
)

router.register(
    "energy-measurements",
    EnergyMeasurementViewSet,
    basename="energy-measurement",
)

urlpatterns = [
    path("", include(router.urls)),
]
