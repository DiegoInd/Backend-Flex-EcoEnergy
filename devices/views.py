from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import InstalledDeviceForm, ZoneForm
from .models import InstalledDevice, Zone


class InstalledDeviceListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = InstalledDevice
    template_name = "devices/installeddevice_list.html"
    context_object_name = "devices"
    permission_required = "devices.view_installeddevice"
    raise_exception = True

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(deleted_at__isnull=True)
            .select_related(
                "product",
                "organization",
                "zone",
            )
        )

        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(
            organization_id=self.request.user.profile.organization_id
        )


class InstalledDeviceCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = InstalledDevice
    form_class = InstalledDeviceForm
    template_name = "devices/installeddevice_form.html"
    permission_required = "devices.add_installeddevice"
    raise_exception = True
    success_url = "/devices/"

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


class InstalledDeviceUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = InstalledDevice
    form_class = InstalledDeviceForm
    template_name = "devices/installeddevice_form.html"
    permission_required = "devices.change_installeddevice"
    raise_exception = True
    success_url = "/devices/"

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


class InstalledDeviceDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = InstalledDevice
    permission_required = "devices.delete_installeddevice"
    raise_exception = True
    success_url = "/devices/"

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


class ZoneListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    model = Zone
    template_name = "devices/zone_list.html"
    context_object_name = "zones"
    permission_required = "devices.view_zone"
    raise_exception = True

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(deleted_at__isnull=True)
            .select_related("organization")
        )

        if self.request.user.is_superuser:
            return queryset

        return queryset.filter(
            organization_id=self.request.user.profile.organization_id
        )


class ZoneCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = Zone
    form_class = ZoneForm
    template_name = "devices/zone_form.html"
    permission_required = "devices.add_zone"
    raise_exception = True
    success_url = "/devices/zones/"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if not self.request.user.is_superuser:
            form.fields["organization"].queryset = (
                form.fields["organization"].queryset.filter(
                    id=self.request.user.profile.organization_id
                )
            )
            form.fields["organization"].initial = (
                self.request.user.profile.organization
            )

        return form

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.organization = (
                self.request.user.profile.organization
            )

        return super().form_valid(form)


class ZoneUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = Zone
    form_class = ZoneForm
    template_name = "devices/zone_form.html"
    permission_required = "devices.change_zone"
    raise_exception = True
    success_url = "/devices/zones/"

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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        if not self.request.user.is_superuser:
            form.fields["organization"].queryset = (
                form.fields["organization"].queryset.filter(
                    id=self.request.user.profile.organization_id
                )
            )

        return form

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.organization = (
                self.request.user.profile.organization
            )

        return super().form_valid(form)


class ZoneDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = Zone
    permission_required = "devices.delete_zone"
    raise_exception = True
    success_url = "/devices/zones/"

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