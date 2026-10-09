from rest_framework import serializers
from accounts.models import Organization
from devices.models import Zone, DeviceProductCatalog, InstalledDevice
from maintenance.models import MaintenanceRequest
from monitoring.models import EnergyMeasurement

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "legal_name",
            "tax_identifier",
            "commercial_name",
            "is_active",
        ]

    def validate_legal_name(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "La razón social debe tener al menos 3 caracteres."
            )

        return value

class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = [
            "id",
            "organization",
            "name",
            "description",
        ]
        read_only_fields = ["id"]

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "El nombre de la zona debe tener al menos 3 caracteres."
            )
        return value.strip()

    def validate_organization(self, value):
        if value.deleted_at is not None:
            raise serializers.ValidationError(
                "No se puede asignar una organización eliminada."
            )
        return value

class DeviceProductCatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeviceProductCatalog
        fields = [
            "id",
            "manufacturer",
            "model_name",
            "sku",
            "specifications",
        ]
        read_only_fields = ["id"]

    def validate_manufacturer(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "El fabricante debe tener al menos 2 caracteres."
            )

        return value

    def validate_model_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "El modelo debe tener al menos 2 caracteres."
            )

        return value
class InstalledDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstalledDevice
        fields = [
            "id",
            "product",
            "organization",
            "zone",
            "internal_name",
            "serial_number",
            "reference_power",
            "status",
            "image",
        ]
        read_only_fields = ["id"]

    def validate_internal_name(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "El nombre interno debe tener al menos 3 caracteres."
            )

        return value

    def validate_reference_power(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "La potencia de referencia debe ser mayor que cero."
            )

        return value

    def validate(self, attrs):
        instance = self.instance

        product = attrs.get(
            "product",
            instance.product if instance else None
        )
        organization = attrs.get(
            "organization",
            instance.organization if instance else None
        )
        zone = attrs.get(
            "zone",
            instance.zone if instance else None
        )

        if product and product.deleted_at is not None:
            raise serializers.ValidationError({
                "product": "No se puede asignar un producto eliminado."
            })

        if organization and organization.deleted_at is not None:
            raise serializers.ValidationError({
                "organization": "No se puede asignar una organización eliminada."
            })

        if zone and zone.deleted_at is not None:
            raise serializers.ValidationError({
                "zone": "No se puede asignar una zona eliminada."
            })

        if zone and organization and zone.organization_id != organization.id:
            raise serializers.ValidationError({
                "zone": "La zona debe pertenecer a la organización seleccionada."
            })

        return attrs
    
class MaintenanceRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaintenanceRequest
        fields = [
            "id",
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
            "created_at",
        ]
        read_only_fields = fields
class EnergyMeasurementSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnergyMeasurement
        fields = [
            "id",
            "device",
            "value",
            "unit",
            "reading_timestamp",
            "source_type",
            "registered_by",
            "created_at",
        ]
        read_only_fields = fields