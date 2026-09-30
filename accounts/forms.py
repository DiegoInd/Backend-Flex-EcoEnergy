from django import forms

from .models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = [
            "legal_name",
            "tax_identifier",
            "commercial_name",
            "is_active",
        ]

        labels = {
            "legal_name": "Razón social",
            "tax_identifier": "RUT / Identificador",
            "commercial_name": "Nombre comercial",
            "is_active": "Activa",
        }

        widgets = {
            "legal_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "tax_identifier": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "commercial_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean_legal_name(self):
        legal_name = self.cleaned_data["legal_name"].strip()

        if len(legal_name) < 3:
            raise forms.ValidationError(
                "La razón social debe tener al menos 3 caracteres."
            )

        return legal_name