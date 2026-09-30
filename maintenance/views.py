from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .forms import MaintenanceRequestForm
from .models import MaintenanceRequest

from django.contrib.auth.decorators import login_required, permission_required
from openpyxl import Workbook
from openpyxl.styles import Font


class MaintenanceRequestListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = MaintenanceRequest
    template_name = "maintenance/maintenance_list.html"
    context_object_name = "maintenance_requests"
    permission_required = "maintenance.view_maintenancerequest"
    raise_exception = True

    def get_paginate_by(self, queryset):
        # Si llega una nueva cantidad por URL, la guardamos en sesión.
        per_page = self.request.GET.get("per_page")

        if per_page:
            try:
                per_page = int(per_page)
            except (TypeError, ValueError):
                per_page = 5

            if per_page not in [5, 15, 30]:
                per_page = 5

            self.request.session["maintenance_per_page"] = per_page

        # Si no llega por URL, usamos lo guardado en la sesión.
        per_page = self.request.session.get(
            "maintenance_per_page",
            5,
        )

        # Seguridad adicional ante un valor inválido en sesión.
        if per_page not in [5, 15, 30]:
            per_page = 5
            self.request.session["maintenance_per_page"] = 5

        return per_page

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(deleted_at__isnull=True)
            .select_related(
                "organization",
                "device",
                "assigned_to",
            )
            .order_by("-created_at")
        )

        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(
            organization_id=self.request.user.profile.organization_id
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["per_page"] = self.request.session.get(
            "maintenance_per_page",
            5,
        )

        return context

class MaintenanceRequestCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = MaintenanceRequest
    form_class = MaintenanceRequestForm
    template_name = "maintenance/maintenance_form.html"
    permission_required = "maintenance.add_maintenancerequest"
    raise_exception = True
    success_url = "/maintenance/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.organization = (
                self.request.user.profile.organization
            )

        return super().form_valid(form)


class MaintenanceRequestUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = MaintenanceRequest
    form_class = MaintenanceRequestForm
    template_name = "maintenance/maintenance_form.html"
    permission_required = "maintenance.change_maintenancerequest"
    raise_exception = True
    success_url = "/maintenance/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(deleted_at__isnull=True)
        )

        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(
            organization_id=self.request.user.profile.organization_id
        )

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.organization = (
                self.request.user.profile.organization
            )

        return super().form_valid(form)


class MaintenanceRequestDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = MaintenanceRequest
    permission_required = "maintenance.delete_maintenancerequest"
    raise_exception = True
    success_url = "/maintenance/"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(deleted_at__isnull=True)
        )

        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(
            organization_id=self.request.user.profile.organization_id
        )

    def form_valid(self, form):
        self.object.deleted_at = timezone.now()
        self.object.save(update_fields=["deleted_at"])

        return HttpResponseRedirect(self.success_url)


@login_required
@permission_required(
    "maintenance.view_maintenancerequest",
    raise_exception=True,
)
def export_maintenance_excel(request):

    queryset = (
        MaintenanceRequest.objects
        .filter(deleted_at__isnull=True)
        .select_related(
            "organization",
            "device",
            "assigned_to",
        )
        .order_by("-created_at")
    )

    if not request.user.is_superuser:
        queryset = queryset.filter(
            organization_id=request.user.profile.organization_id
        )

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Mantenimientos"

    headers = [
        "ID",
        "Dispositivo",
        "Organización",
        "Motivo",
        "Prioridad",
        "Estado",
        "Asignado a",
        "Costo",
        "Fecha de creación",
    ]

    worksheet.append(headers)

    for cell in worksheet[1]:
        cell.font = Font(bold=True)

    priority_labels = {
        "low": "Baja",
        "medium": "Media",
        "high": "Alta",
    }

    status_labels = {
        "pending": "Pendiente",
        "in_progress": "En progreso",
        "closed": "Cerrada",
    }

    for maintenance in queryset:

        assigned_to = (
            maintenance.assigned_to.username
            if maintenance.assigned_to
            else "Sin asignar"
        )

        created_at = maintenance.created_at

        if created_at:
            created_at = timezone.localtime(
                created_at
            ).strftime("%d-%m-%Y %H:%M")

        worksheet.append([
            maintenance.id,
            maintenance.device.internal_name,
            str(maintenance.organization),
            maintenance.reason,
            priority_labels.get(
                maintenance.priority,
                maintenance.priority,
            ),
            status_labels.get(
                maintenance.status,
                maintenance.status,
            ),
            assigned_to,
            maintenance.cost if maintenance.cost is not None else 0,
            created_at,
        ])

    column_widths = {
        "A": 10,
        "B": 30,
        "C": 30,
        "D": 45,
        "E": 15,
        "F": 18,
        "G": 20,
        "H": 15,
        "I": 22,
    }

    for column, width in column_widths.items():
        worksheet.column_dimensions[column].width = width

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    response["Content-Disposition"] = (
        'attachment; filename="mantenimientos_ecoenergy.xlsx"'
    )

    workbook.save(response)

    return response