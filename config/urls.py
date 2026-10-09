"""
URL configuration for config project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Unidad 3 - Autenticación JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path("admin/", admin.site.urls),

    # Unidad 3 - API REST
    path("api/", include("api.urls")),

    # Unidad 3 - Tokens JWT
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

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