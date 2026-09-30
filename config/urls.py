"""
URL configuration for config project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),

    # Autenticación de Django
    path("accounts/", include("django.contrib.auth.urls")),

    # Recuperación de contraseña y CRUD de organizaciones
    path("accounts/", include("accounts.urls")),

    # CRUD de dispositivos y zonas
    path("devices/", include("devices.urls")),

    # CRUD de mantenimiento
    path("maintenance/", include("maintenance.urls")),

    # Aplicación principal
    path("", include("dispositivos.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )