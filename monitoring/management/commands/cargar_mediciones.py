from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from devices.models import InstalledDevice
from monitoring.models import EnergyMeasurement


class Command(BaseCommand):
    help = "Carga 1000 mediciones de prueba sin duplicarlas."

    def handle(self, *args, **options):
        marcador = "seed_u3_"

        existentes = EnergyMeasurement.objects.filter(
            source_type__startswith=marcador
        ).count()

        if existentes:
            self.stdout.write(
                self.style.WARNING(
                    "Ya existen mediciones de esta carga. "
                    "No se crearán duplicados."
                )
            )
            return

        dispositivos = list(
            InstalledDevice.objects.filter(
                deleted_at__isnull=True
            ).order_by("id")
        )

        if not dispositivos:
            raise CommandError(
                "No hay dispositivos activos para registrar mediciones."
            )

        fecha_base = timezone.now()
        mediciones = []

        for numero in range(1000):
            dispositivo = dispositivos[numero % len(dispositivos)]

            mediciones.append(
                EnergyMeasurement(
                    device=dispositivo,
                    value=100.0 + (numero % 250),
                    unit="kWh",
                    reading_timestamp=fecha_base - timedelta(
                        minutes=numero
                    ),
                    source_type=f"{marcador}demo",
                    registered_by=None,
                )
            )

        with transaction.atomic():
            EnergyMeasurement.objects.bulk_create(
                mediciones,
                batch_size=200,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Se crearon 1000 mediciones correctamente."
            )
        )