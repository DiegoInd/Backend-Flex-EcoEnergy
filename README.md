# EcoEnergy — Evaluación Sumativa 3: API REST con JWT

Proyecto académico desarrollado con **Django 6.1**, **Django REST Framework**, **Simple JWT** y **MariaDB**. La API REST de la Unidad 3 se incorpora al proyecto web de la Unidad 2 **sin sustituir sus módulos ni migraciones**.

## 1. Requisitos

- Python 3.12 o superior (desarrollo y pruebas: Python 3.13).
- Git y MariaDB Server.
- Dependencias de `requirements.txt`, incluyendo `djangorestframework==3.18.3` y `djangorestframework-simplejwt==5.5.1`.
- Apidog para ejecutar y documentar las pruebas de la evaluación.

## 2. Instalación en otro computador

Clonar el repositorio colaborativo:

```bash
git clone https://github.com/DiegoInd/Backend-Flex-EcoEnergy.git
cd Backend-Flex-EcoEnergy
```

> **Importante:** verificar que la rama entregada incluya los cambios de la Unidad 3 (`feature/api-rest-jwt`) o que estos se hayan integrado a la rama principal. Clonar por sí solo no garantiza que se obtenga esa rama.

Crear y activar el entorno virtual en Windows con Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

En Windows CMD, la activación es `.venv\Scripts\activate`. En macOS/Linux, `source .venv/bin/activate`.

### Configuración de MariaDB

Crear una base de datos vacía:

```sql
CREATE DATABASE ecoenergy_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Copiar `.env.example` a `.env` y configurar los valores propios del equipo. Variables utilizadas:

```dotenv
SECRET_KEY=una_clave_local_segura
DB_ENGINE=django.db.backends.mysql
DB_NAME=ecoenergy_db
DB_USER=root
DB_PASSWORD=CONTRASENA_LOCAL_MARIADB
DB_HOST=127.0.0.1
DB_PORT=3307
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=CORREO_DE_PRUEBA
EMAIL_HOST_PASSWORD=CLAVE_DE_APLICACION_LOCAL
DEFAULT_FROM_EMAIL=CORREO_DE_PRUEBA
```

El puerto `3307` corresponde a la configuración de desarrollo; si el servidor usa `3306`, modificar `DB_PORT`. **Nunca subir el archivo `.env` ni contraseñas reales de servicios a GitHub.**

Aplicar migraciones y verificar:

```bash
python manage.py migrate
python manage.py check
python manage.py runserver
```

Servidor local: `http://127.0.0.1:8000/`. Administración de Django: `http://127.0.0.1:8000/admin/`.

> Las migraciones crean la estructura, **no copian automáticamente** los datos ni las cuentas del computador de desarrollo. En una instalación nueva deben prepararse los datos base y usuarios de demostración antes de ejecutar los comandos de carga.

## 3. API REST — Seis modelos

**URL base:** `http://127.0.0.1:8000/api/`

| Tipo | Modelo | Ruta de lista | Operaciones |
|---|---|---|---|
| Principal | `Organization` | `/api/organizations/` | GET, POST, PUT, PATCH, DELETE |
| Principal | `Zone` | `/api/zones/` | GET, POST, PUT, PATCH, DELETE |
| Principal | `DeviceProductCatalog` | `/api/device-products/` | GET, POST, PUT, PATCH, DELETE |
| Principal | `InstalledDevice` | `/api/installed-devices/` | GET, POST, PUT, PATCH, DELETE |
| Operacional | `MaintenanceRequest` | `/api/maintenance-requests/` | GET lista y detalle |
| Operacional | `EnergyMeasurement` | `/api/energy-measurements/` | GET lista y detalle |

Para operaciones sobre un registro, añadir su ID: por ejemplo, `GET /api/energy-measurements/1/` o `PATCH /api/organizations/1/`.

Los cuatro modelos principales utilizan `ModelViewSet` y **eliminación lógica**: DELETE marca `deleted_at`, sin borrar físicamente la fila. Los dos operacionales utilizan `ReadOnlyModelViewSet` y no aceptan POST, PUT, PATCH ni DELETE.

## 4. Autenticación JWT

### Obtener access y refresh

**POST** `http://127.0.0.1:8000/api/token/`

```json
{
  "username": "consulta",
  "password": "EcoEnergy#2026"
}
```

La respuesta correcta contiene `access` y `refresh`. En Apidog, enviar el token de acceso en cada petición protegida:

```text
Authorization: Bearer <ACCESS_TOKEN>
```

### Renovar access

**POST** `http://127.0.0.1:8000/api/token/refresh/`

```json
{
  "refresh": "<REFRESH_TOKEN>"
}
```

Prueba realizada: HTTP **200** y presencia de un nuevo campo `access`.

## 5. Usuarios de demostración y contraseñas

**Solo para la evaluación académica local.** Las siguientes contraseñas se indican para facilitar las pruebas; `admin` y `api_sin_rol` fueron restablecidos mediante `changepassword`. El mensaje de éxito de Django no permite ver qué texto se escribió, así que confirmar el inicio de sesión si alguna credencial no funciona.

| Usuario | Contraseña de prueba prevista | Rol / uso |
|---|---|---|
| `admin` | `EcoEnergy#2026Admin` | Superusuario general de Django; administración web |
| `admin_organizacion` | `EcoEnergy#2026` | Grupo `api_admin`; CRUD de la API |
| `consulta` | `EcoEnergy#2026` | Grupo `api_operador`; GET en la API |
| `api_sin_rol` | `EcoEnergy#2026` | Sin grupo; prueba de HTTP 403 |

Los tres usuarios de prueba de roles de API (`admin_organizacion`, `consulta`, `api_sin_rol`) se comprobaron **activos y no superusuarios**. `admin` es una cuenta diferente y conserva el rol de superadministrador de Django.

**Advertencia:** estas credenciales no deben reutilizarse en producción ni en servicios expuestos a Internet. Si este README se publica, las contraseñas también se hacen públicas; cambiarlas o retirarlas antes de un despliegue real.

## 6. Permisos

El permiso personalizado `IsAPIAdminOrReadOnlyOperator` establece:

- **Sin token:** HTTP `401 Unauthorized`.
- **Usuario sin grupo de API:** HTTP `403 Forbidden`.
- **`api_operador`:** puede consultar mediante GET; no puede crear, editar ni eliminar (`403` para POST en los modelos principales).
- **`api_admin`:** puede consultar y realizar CRUD en los cuatro modelos principales.
- **Endpoints operacionales:** solo GET; POST devuelve `405 Method Not Allowed` incluso para `api_admin`.

## 7. Validaciones

Los serializers comprueban, entre otros aspectos:

- Razón social y nombres de zona con longitud mínima.
- Fabricante y modelo del producto con longitud mínima.
- Nombre interno del dispositivo con longitud mínima.
- `reference_power` mayor que cero.
- No asignar organización, producto o zona eliminados lógicamente.
- La zona debe pertenecer a la organización seleccionada.

Los datos inválidos generan HTTP `400 Bad Request`; un recurso inexistente o eliminado lógicamente devuelve `404 Not Found`.

## 8. Paginación

La API utiliza `PageNumberPagination` con **20 registros por página**. Ejemplo:

```text
GET /api/maintenance-requests/?page=2
```

La respuesta incluye `count`, `next`, `previous` y `results`. Se comprobó `HTTP 200`, `count = 1000`, `len(results) = 20` y `next` apuntando a `?page=2`.

## 9. Datos de prueba reproducibles

El proyecto conserva el comando de la Unidad 2:

```bash
python manage.py seed_data
```

Este comando prepara datos de demostración, incluidas solicitudes de mantenimiento, según su implementación y los datos base disponibles.

Para la Unidad 3 se agregó:

```bash
python manage.py cargar_mediciones
```

Archivo: `monitoring/management/commands/cargar_mediciones.py`.

Crea **1.000 mediciones** asociadas a dispositivos activos existentes, con marcador `seed_u3_demo`. Si detecta una carga previa, evita crearla otra vez. **Requiere que ya existan dispositivos activos.**

### Conteo verificado en la base de desarrollo

| Modelo | Activos |
|---|---:|
| Organization | 1 |
| Zone | 4 |
| DeviceProductCatalog | 2 |
| InstalledDevice | 4 |
| MaintenanceRequest | 1.000 |
| EnergyMeasurement | 1.003 |
| **Total** | **2.014** |

Se superó el mínimo de **2.000 registros activos**. Este conteo corresponde a la base de datos de desarrollo; no implica que un clon nuevo ya incluya esos registros.

## 10. Pruebas HTTP realizadas

| Código | Caso |
|---|---|
| `200 OK` | GET de listas y detalles; PATCH correcto; refresh JWT |
| `201 Created` | POST válido de modelo principal |
| `204 No Content` | DELETE lógico de modelo principal |
| `400 Bad Request` | Validaciones de campos y relaciones |
| `401 Unauthorized` | Solicitud sin JWT |
| `403 Forbidden` | Usuario sin rol o escritura por operador |
| `404 Not Found` | Registro inexistente o eliminado lógicamente |
| `405 Method Not Allowed` | POST en `energy-measurements` con administrador |

Se verificaron la paginación, las tres cuentas de prueba de roles, los **2.014 registros activos** y la prevención de duplicados del comando de mediciones.

## 11. Apidog — Evidencias de evaluación

La colección y las capturas de Apidog **aún están pendientes de preparar**. Deben incluir:

1. Obtención y renovación de JWT.
2. GET lista y detalle de los seis modelos.
3. POST, PATCH/PUT y DELETE de los cuatro modelos principales.
4. Errores `400`, `401`, `403`, `404` y `405`, según corresponda.
5. Paginación y respuestas de datos.
6. Exportación de la colección y evidencias solicitadas por el docente.

## 12. Comandos de comprobación

```bash
python manage.py check
python manage.py showmigrations
python manage.py runserver
```

Para verificar el conteo de datos se puede utilizar `python manage.py shell` y consultar los modelos activos (`deleted_at__isnull=True`).

## 13. Archivos importantes

- `config/settings.py`: Django REST Framework, JWT y paginación.
- `config/urls.py`: rutas generales y tokens.
- `api/urls.py`: rutas REST.
- `api/views.py`: ViewSets y eliminación lógica.
- `api/serializers.py`: campos y validaciones.
- `api/permissions.py`: autorización por grupos.
- `monitoring/management/commands/cargar_mediciones.py`: carga reproducible.
- `requirements.txt`: dependencias.
- `.env.example`: plantilla de configuración sin secretos reales.

**Nota:** el proyecto web original de la Unidad 2 sigue presente; este README prioriza las rutas REST que se evaluarán en la Unidad 3.
