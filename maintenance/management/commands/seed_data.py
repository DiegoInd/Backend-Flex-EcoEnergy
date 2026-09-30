from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Organization
from devices.models import (
    DeviceProductCatalog,
    InstalledDevice,
    Zone,
)
from maintenance.models import MaintenanceRequest


User = get_user_model()


class Command(BaseCommand):
    help = "Genera 1000 registros de mantenimiento para pruebas."

    def handle(self, *args, **options):

        # Organización principal
        organization = (
            Organization.objects
            .filter(
                deleted_at__isnull=True,
                is_active=True,
            )
            .first()
        )

        if not organization:
            self.stdout.write(
                self.style.ERROR(
                    "No existe una organización activa."
                )
            )
            return

        # Zona para los dispositivos de prueba
        zone, _ = Zone.objects.get_or_create(
            organization=organization,
            name="Zona Seed",
            defaults={
                "description": (
                    "Zona creada automáticamente para datos de prueba."
                )
            },
        )

        # Producto del catálogo
        product, _ = DeviceProductCatalog.objects.get_or_create(
            sku="SEED-PM-001",
            defaults={
                "manufacturer": "EcoEnergy",
                "model_name": "Medidor Seed",
                "specifications": (
                    "Dispositivo utilizado para datos de prueba."
                ),
            },
        )

        # Dispositivo para los mantenimientos
        device, _ = InstalledDevice.objects.get_or_create(
            serial_number="SEED-DEVICE-001",
            defaults={
                "product": product,
                "organization": organization,
                "zone": zone,
                "internal_name": "Medidor Seed",
                "reference_power": 100.0,
                "status": "active",
            },
        )

        # Usuario para asignación
        user = User.objects.filter(
            is_superuser=True
        ).first()

        if not user:
            user = User.objects.filter(
                is_active=True
            ).first()

        priorities = [
            "low",
            "medium",
            "high",
        ]

        statuses = [
            "pending",
            "in_progress",
            "closed",
        ]

        created_count = 0

        for number in range(1, 1001):

            reason = (
                f"Mantenimiento preventivo de prueba #{number}"
            )

            # Evita duplicar los registros si el comando
            # se ejecuta nuevamente.
            _, created = MaintenanceRequest.objects.get_or_create(
                organization=organization,
                device=device,
                reason=reason,
                defaults={
                    "priority": priorities[
                        (number - 1) % len(priorities)
                    ],
                    "status": statuses[
                        (number - 1) % len(statuses)
                    ],
                    "assigned_to": user,
                    "scheduled_date": timezone.now(),
                    "diagnosis_notes": (
                        f"Registro de prueba generado "
                        f"automáticamente #{number}"
                    ),
                    "cost": Decimal(
                        10000 + (number * 10)
                    ),
                },
            )

            if created:
                created_count += 1

        total = MaintenanceRequest.objects.filter(
            deleted_at__isnull=True
        ).count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed completado. "
                f"Nuevos registros: {created_count}. "
                f"Total activos: {total}."
            )
        )