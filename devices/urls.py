from django.urls import path

from .views import (
    InstalledDeviceCreateView,
    InstalledDeviceDeleteView,
    InstalledDeviceListView,
    InstalledDeviceUpdateView,
    ZoneListView,
    ZoneCreateView,
    ZoneUpdateView,
    ZoneDeleteView,
)


urlpatterns = [
    # Dispositivos
    path(
        "",
        InstalledDeviceListView.as_view(),
        name="installeddevice_list",
    ),
    path(
        "create/",
        InstalledDeviceCreateView.as_view(),
        name="installeddevice_create",
    ),
    path(
        "<int:pk>/edit/",
        InstalledDeviceUpdateView.as_view(),
        name="installeddevice_update",
    ),
    path(
        "<int:pk>/delete/",
        InstalledDeviceDeleteView.as_view(),
        name="installeddevice_delete",
    ),

    # Zonas
    path(
        "zones/",
        ZoneListView.as_view(),
        name="zone_list",
    ),
    path(
        "zones/create/",
        ZoneCreateView.as_view(),
        name="zone_create",
    ),
    path(
        "zones/<int:pk>/edit/",
        ZoneUpdateView.as_view(),
        name="zone_update",
    ),
    path(
        "zones/<int:pk>/delete/",
        ZoneDeleteView.as_view(),
        name="zone_delete",
    ),
]