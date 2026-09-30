from django.urls import path

from .views import (
    MaintenanceRequestCreateView,
    MaintenanceRequestDeleteView,
    MaintenanceRequestListView,
    MaintenanceRequestUpdateView,
    export_maintenance_excel,
)


urlpatterns = [
    path(
        "",
        MaintenanceRequestListView.as_view(),
        name="maintenance_list",
    ),
    path(
        "create/",
        MaintenanceRequestCreateView.as_view(),
        name="maintenance_create",
    ),
    path(
        "export/excel/",
        export_maintenance_excel,
        name="maintenance_export_excel",
    ),
    path(
        "<int:pk>/edit/",
        MaintenanceRequestUpdateView.as_view(),
        name="maintenance_update",
    ),
    path(
        "<int:pk>/delete/",
        MaintenanceRequestDeleteView.as_view(),
        name="maintenance_delete",
    ),
]