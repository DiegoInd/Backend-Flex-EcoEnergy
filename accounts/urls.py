from django.urls import path
from . import views

urlpatterns = [
    # CLASE 6 - Recuperación de contraseña
    path(
        "password-reset/",
        views.password_reset_request,
        name="password_reset_request",
    ),
    path(
        "password-reset/verify/",
        views.password_reset_verify,
        name="password_reset_verify",
    ),
    path(
        "password-reset/confirm/",
        views.password_reset_confirm,
        name="password_reset_confirm",
    ),

    # CLASE 7 - CRUD de organizaciones
    path(
        "organizations/",
        views.OrganizationListView.as_view(),
        name="organization_list",
    ),
    path(
        "organizations/create/",
        views.OrganizationCreateView.as_view(),
        name="organization_create",
    ),
    path(
        "organizations/<int:pk>/edit/",
        views.OrganizationUpdateView.as_view(),
        name="organization_update",
    ),
    path(
        "organizations/<int:pk>/delete/",
        views.OrganizationDeleteView.as_view(),
        name="organization_delete",
    ),
]