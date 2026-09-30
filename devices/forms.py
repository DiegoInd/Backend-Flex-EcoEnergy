from pathlib import Path

from django import forms
from PIL import Image

from .models import InstalledDevice,Zone


class InstalledDeviceForm(forms.ModelForm):
    class Meta:
        model = InstalledDevice
        fields = [
            "product",
            "organization",
            "zone",
            "internal_name",
            "serial_number",
            "reference_power",
            "status",
            "image",
        ]

        labels = {
            "product": "Producto",
            "organization": "Organización",
            "zone": "Zona",
            "internal_name": "Nombre interno",
            "serial_number": "Número de serie",
            "reference_power": "Potencia de referencia",
            "status": "Estado",
            "image": "Imagen",
        }

        widgets = {
            "product": forms.Select(
                attrs={"class": "form-select"}
            ),
            "organization": forms.Select(
                attrs={"class": "form-select"}
            ),
            "zone": forms.Select(
                attrs={"class": "form-select"}
            ),
            "internal_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "serial_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "reference_power": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "status": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".jpg,.jpeg,.png",
                }
            ),
        }
        error_messages = {
            "image": {
                "invalid_image": (
                    "Sube una imagen válida. El archivo seleccionado "
                    "no es una imagen o está dañado."
                ),
            },
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

            self.fields["zone"].queryset = (
                self.fields["zone"].queryset.filter(
                    organization=organization,
                    deleted_at__isnull=True,
                )
            )

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if not image:
            return image

        # Máximo 5 MB
        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "La imagen no puede superar los 5 MB."
            )

        # Extensiones permitidas
        extension = Path(image.name).suffix.lower()

        if extension not in [".jpg", ".jpeg", ".png"]:
            raise forms.ValidationError(
                "Solo se permiten imágenes JPG, JPEG o PNG."
            )

        # Verificar que el archivo sea realmente una imagen
        try:
            img = Image.open(image)
            img.verify()
        except Exception:
            raise forms.ValidationError(
                "El archivo seleccionado no es una imagen válida."
            )

        image.seek(0)

        return image

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = [
            "organization",
            "name",
            "description",
        ]

        labels = {
            "organization": "Organización",
            "name": "Nombre",
            "description": "Descripción",
        }

        widgets = {
            "organization": forms.Select(
                attrs={"class": "form-select"}
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ej: Sala de Servidores",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Descripción de la zona",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 3:
            raise forms.ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )

        return name