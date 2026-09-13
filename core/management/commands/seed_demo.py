from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.utils import timezone

from accounts.models import Organization, Department, UserProfile
from devices.models import Zone, DeviceProductCatalog, InstalledDevice
from monitoring.models import EnergyMeasurement
from maintenance.models import MaintenanceRequest


class Command(BaseCommand):
    help = "Carga datos de demostración para la evaluación de EcoEnergy"

    def handle(self, *args, **options):

        self.stdout.write("Cargando datos de demostración EcoEnergy...")

        # =========================================================
        # 1. ORGANIZACIONES
        # =========================================================

        org_chile, _ = Organization.objects.update_or_create(
            tax_identifier="76123456-7",
            defaults={
                "legal_name": "EcoEnergy Chile SpA",
                "commercial_name": "EcoEnergy Chile",
                "is_active": True,
            },
        )

        org_norte, _ = Organization.objects.update_or_create(
            tax_identifier="76987654-3",
            defaults={
                "legal_name": "EcoEnergy Norte SpA",
                "commercial_name": "EcoEnergy Norte",
                "is_active": True,
            },
        )

        # =========================================================
        # 2. DEPARTAMENTOS
        # =========================================================

        dep_chile, _ = Department.objects.update_or_create(
            organization=org_chile,
            name="Operaciones",
            defaults={
                "description": "Departamento de operaciones EcoEnergy Chile",
                "is_active": True,
            },
        )

        dep_norte, _ = Department.objects.update_or_create(
            organization=org_norte,
            name="Departamento Norte",
            defaults={
                "description": "Departamento de operaciones EcoEnergy Norte",
                "is_active": True,
            },
        )

        # =========================================================
        # 3. ZONAS
        # =========================================================

        zona_chile, _ = Zone.objects.update_or_create(
            organization=org_chile,
            name="Sala Servidores",
            defaults={
                "description": "Zona principal de medición",
            },
        )

        zona_norte, _ = Zone.objects.update_or_create(
            organization=org_norte,
            name="Zona Norte",
            defaults={
                "description": "Zona de prueba para EcoEnergy Norte",
            },
        )

        # =========================================================
        # 4. CATÁLOGO DE PRODUCTOS
        # =========================================================

        producto, _ = DeviceProductCatalog.objects.update_or_create(
            sku="PM5000-001",
            defaults={
                "manufacturer": "Schneider Electric",
                "model_name": "Power Meter PM5000",
                "specifications": "Medidor de energía para monitoreo eléctrico",
            },
        )

        # =========================================================
        # 5. DISPOSITIVOS
        # =========================================================

        dispositivo_chile, _ = InstalledDevice.objects.update_or_create(
            serial_number="SN-ECO-001",
            defaults={
                "product": producto,
                "organization": org_chile,
                "zone": zona_chile,
                "internal_name": "Medidor Sala Servidores",
                "reference_power": 5.0,
                "status": "active",
            },
        )

        dispositivo_norte, _ = InstalledDevice.objects.update_or_create(
            serial_number="SN-NORTE-001",
            defaults={
                "product": producto,
                "organization": org_norte,
                "zone": zona_norte,
                "internal_name": "Medidor Norte",
                "reference_power": 5.0,
                "status": "active",
            },
        )

        # =========================================================
        # 6. GRUPO ADMINISTRADOR ORGANIZACIONAL
        # =========================================================

        grupo_admin, _ = Group.objects.get_or_create(
            name="Administrador organizacional"
        )

        permisos_admin = Permission.objects.filter(
            codename__in=[
                "view_organization",
                "change_organization",

                "add_department",
                "change_department",
                "view_department",

                "add_userprofile",
                "change_userprofile",
                "view_userprofile",

                "add_zone",
                "change_zone",
                "view_zone",

                "view_deviceproductcatalog",

                "add_installeddevice",
                "change_installeddevice",
                "view_installeddevice",

                "add_energymeasurement",
                "change_energymeasurement",
                "view_energymeasurement",

                "add_maintenancerequest",
                "change_maintenancerequest",
                "view_maintenancerequest",
            ]
        )

        grupo_admin.permissions.set(permisos_admin)

        # =========================================================
        # 7. GRUPO CONSULTA
        # =========================================================

        grupo_consulta, _ = Group.objects.get_or_create(
            name="Consulta"
        )

        permisos_consulta = Permission.objects.filter(
            codename__in=[
                "view_installeddevice",
                "view_energymeasurement",
            ]
        )

        grupo_consulta.permissions.set(permisos_consulta)

        # =========================================================
        # 8. USUARIO ADMINISTRADOR DE PRUEBA
        # =========================================================

        admin_demo, _ = User.objects.get_or_create(
            username="admin_demo"
        )

        admin_demo.email = "admin.demo@ecoenergy.cl"
        admin_demo.is_staff = True
        admin_demo.is_superuser = True
        admin_demo.is_active = True
        admin_demo.set_password("EcoEnergy2026!")
        admin_demo.save()

        # =========================================================
        # 9. USUARIO LIMITADO
        # =========================================================

        usuario_limitado, _ = User.objects.get_or_create(
            username="admin_organizacion"
        )

        usuario_limitado.email = "admin.organizacion@ecoenergy.cl"
        usuario_limitado.is_staff = True
        usuario_limitado.is_superuser = False
        usuario_limitado.is_active = True
        usuario_limitado.set_password("EcoEnergy2026!")
        usuario_limitado.save()

        usuario_limitado.groups.set([grupo_admin])

        UserProfile.objects.update_or_create(
            user=usuario_limitado,
            defaults={
                "organization": org_chile,
                "department": dep_chile,
                "employee_code": "EMP-004",
                "phone": "+56911111111",
            },
        )

        # =========================================================
        # 10. USUARIO DE CONSULTA
        # =========================================================

        consulta, _ = User.objects.get_or_create(
            username="consulta"
        )

        consulta.email = "consulta@ecoenergy.cl"
        consulta.is_staff = True
        consulta.is_superuser = False
        consulta.is_active = True
        consulta.set_password("EcoEnergy2026!")
        consulta.save()

        consulta.groups.set([grupo_consulta])

        UserProfile.objects.update_or_create(
            user=consulta,
            defaults={
                "organization": org_chile,
                "department": dep_chile,
                "employee_code": "EMP-003",
                "phone": "+56922222222",
            },
        )

        # =========================================================
        # 11. MEDICIONES
        # =========================================================

        EnergyMeasurement.objects.get_or_create(
            device=dispositivo_chile,
            value=125.5,
            unit="kWh",
            source_type="manual",
            defaults={
                "reading_timestamp": timezone.now(),
                "registered_by": admin_demo,
            },
        )

        EnergyMeasurement.objects.get_or_create(
            device=dispositivo_norte,
            value=200.0,
            unit="kWh",
            source_type="manual",
            defaults={
                "reading_timestamp": timezone.now(),
                "registered_by": admin_demo,
            },
        )

        # =========================================================
        # 12. MANTENIMIENTOS
        # =========================================================

        MaintenanceRequest.objects.get_or_create(
            organization=org_chile,
            device=dispositivo_chile,
            reason="Revisión preventiva del medidor",
            defaults={
                "priority": "medium",
                "status": "pending",
                "assigned_to": usuario_limitado,
                "scheduled_date": timezone.now(),
                "diagnosis_notes": "Mantenimiento de prueba para evaluación",
                "cost": 25000,
            },
        )

        MaintenanceRequest.objects.get_or_create(
            organization=org_norte,
            device=dispositivo_norte,
            reason="Revisión preventiva zona norte",
            defaults={
                "priority": "high",
                "status": "pending",
                "assigned_to": admin_demo,
                "scheduled_date": timezone.now(),
                "diagnosis_notes": "Registro para comprobar scoping",
                "cost": 30000,
            },
        )

        # =========================================================
        # FINAL
        # =========================================================

        self.stdout.write(
            self.style.SUCCESS(
                "\nDatos de demostración cargados correctamente."
            )
        )

        self.stdout.write("")
        self.stdout.write("CUENTAS DE PRUEBA")
        self.stdout.write("-------------------------------")
        self.stdout.write("Administrador:")
        self.stdout.write("Usuario: admin_demo")
        self.stdout.write("Clave: EcoEnergy2026!")
        self.stdout.write("")
        self.stdout.write("Administrador organizacional:")
        self.stdout.write("Usuario: admin_organizacion")
        self.stdout.write("Clave: EcoEnergy2026!")
        self.stdout.write("")
        self.stdout.write("Consulta:")
        self.stdout.write("Usuario: consulta")
        self.stdout.write("Clave: EcoEnergy2026!")