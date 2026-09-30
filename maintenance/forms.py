from django import forms

from .models import MaintenanceRequest


class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest

        fields = [
            "organization",
            "device",
            "reason",
            "priority",
            "status",
            "assigned_to",
            "scheduled_date",
            "actual_completion_date",
            "diagnosis_notes",
            "cost",
        ]

        labels = {
            "organization": "Organización",
            "device": "Dispositivo",
            "reason": "Motivo",
            "priority": "Prioridad",
            "status": "Estado",
            "assigned_to": "Asignado a",
            "scheduled_date": "Fecha programada",
            "actual_completion_date": "Fecha de finalización",
            "diagnosis_notes": "Notas de diagnóstico",
            "cost": "Costo",
        }

        widgets = {
            "organization": forms.Select(
                attrs={"class": "form-select"}
            ),
            "device": forms.Select(
                attrs={"class": "form-select"}
            ),
            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "priority": forms.Select(
                choices=[
                    ("low", "Baja"),
                    ("medium", "Media"),
                    ("high", "Alta"),
                ],
                attrs={"class": "form-select"},
            ),
            "status": forms.Select(
                choices=[
                    ("pending", "Pendiente"),
                    ("in_progress", "En progreso"),
                    ("closed", "Cerrada"),
                ],
                attrs={"class": "form-select"},
            ),
            "assigned_to": forms.Select(
                attrs={"class": "form-select"}
            ),
            "scheduled_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
            "actual_completion_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                }
            ),
            "diagnosis_notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "cost": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user and not user.is_superuser:
            organization = user.profile.organization

            self.fields["organization"].queryset = (
                self.fields["organization"].queryset.filter(
                    id=organization.id,
                    deleted_at__isnull=True,
                )
            )

            self.fields["organization"].initial = organization
            self.fields["organization"].disabled = True

            self.fields["device"].queryset = (
                self.fields["device"].queryset.filter(
                    organization=organization,
                    deleted_at__isnull=True,
                )
            )

    def clean_reason(self):
        reason = self.cleaned_data["reason"].strip()

        if len(reason) < 5:
            raise forms.ValidationError(
                "El motivo debe tener al menos 5 caracteres."
            )

        return reason

    def clean_cost(self):
        cost = self.cleaned_data.get("cost")

        if cost is not None and cost < 0:
            raise forms.ValidationError(
                "El costo no puede ser negativo."
            )

        return cost

    def clean(self):
        cleaned_data = super().clean()

        organization = cleaned_data.get("organization")
        device = cleaned_data.get("device")

        if (
            organization
            and device
            and device.organization_id != organization.id
        ):
            self.add_error(
                "device",
                "El dispositivo debe pertenecer a la organización seleccionada.",
            )

        return cleaned_data