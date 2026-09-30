# Backend-Flex-EcoEnergy

## Descripción

EcoEnergy es una aplicación web desarrollada con Django para administrar organizaciones, departamentos, zonas, dispositivos, mediciones de energía y solicitudes de mantenimiento.

El sistema utiliza MariaDB como base de datos e implementa autenticación, recuperación de contraseña, permisos, restricciones de acceso por organización, eliminación lógica, carga de imágenes, paginación y exportación de información a Excel.

---

# Requisitos

Antes de clonar y ejecutar el proyecto en un computador nuevo se debe tener instalado:

- Git
- Python 3.12 o superior
- MariaDB Server
- pip

Las dependencias de Python utilizadas por el proyecto se instalan automáticamente desde `requirements.txt`.

Entre las principales se encuentran:

- Django 6.1
- mysqlclient
- python-dotenv
- Pillow
- openpyxl

---

# 1. Clonar el repositorio

Abrir Git Bash y ejecutar:

```bash
git clone https://github.com/DiegoInd/Backend-Flex-EcoEnergy.git
cd Backend-Flex-EcoEnergy
```

---

# 2. Crear el entorno virtual

En Windows utilizando Git Bash:

```bash
python -m venv .venv
```

Activar el entorno:

```bash
source .venv/Scripts/activate
```

Si se utiliza CMD:

```text
.venv\Scripts\activate
```

En macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

# 3. Instalar las dependencias

Con el entorno virtual activado ejecutar:

```bash
pip install -r requirements.txt
```

No es necesario instalar Django, Pillow, openpyxl o mysqlclient individualmente si la instalación mediante `requirements.txt` finaliza correctamente.

---

# 4. Instalar y preparar MariaDB

MariaDB Server debe estar instalado y ejecutándose en el computador.

El proyecto utiliza una base de datos llamada:

```text
ecoenergy_db
```

Ingresar a MariaDB y crear la base de datos:

```sql
CREATE DATABASE ecoenergy_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

El computador utilizado durante el desarrollo tiene MariaDB configurado en:

```text
Host: 127.0.0.1
Puerto: 3307
```

Si MariaDB se encuentra configurado en otro puerto, por ejemplo `3306`, solamente se debe cambiar `DB_PORT` en el archivo `.env`.

Cada computador debe utilizar su propia contraseña de MariaDB.

---

# 5. Configurar las variables de entorno

El repositorio incluye:

```text
.env.example
```

Este archivo sirve como referencia.

Crear en la raíz del proyecto un archivo llamado:

```text
.env
```

Utilizar como base:

```env
SECRET_KEY=tu_clave_secreta_aqui

DB_ENGINE=django.db.backends.mysql
DB_NAME=ecoenergy_db
DB_USER=root
DB_PASSWORD=tu_password_mariadb
DB_HOST=127.0.0.1
DB_PORT=3307

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_password_de_aplicacion
DEFAULT_FROM_EMAIL=tu_correo@gmail.com
```

Se deben reemplazar los valores de ejemplo por los correspondientes al computador donde se ejecutará el proyecto.

El archivo `.env` contiene información privada y NO debe subirse a GitHub.

---

# 6. Configuración del correo electrónico

La recuperación de contraseña permite enviar un código de 6 dígitos por correo electrónico.

Para utilizar el envío real mediante Gmail se deben configurar en `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_password_de_aplicacion
DEFAULT_FROM_EMAIL=tu_correo@gmail.com
```

`EMAIL_HOST_PASSWORD` corresponde a una contraseña de aplicación configurada para la cuenta de correo utilizada por el proyecto.

La contraseña de aplicación real no debe almacenarse en GitHub.

---

# 7. Aplicar las migraciones

Con MariaDB funcionando y `.env` configurado ejecutar:

```bash
python manage.py migrate
```

Comprobar las migraciones:

```bash
python manage.py showmigrations
```

Luego verificar el proyecto:

```bash
python manage.py check
```

El resultado esperado es:

```text
System check identified no issues (0 silenced).
```

---

# 8. Generar datos de prueba

El proyecto incluye un Management Command para generar 1000 solicitudes de mantenimiento utilizadas durante las pruebas y evaluación del sistema.

Antes de ejecutar este comando deben existir los datos base del sistema, incluyendo una organización activa.

Ejecutar:

```bash
python manage.py seed_data
```

El comando genera 1000 solicitudes de mantenimiento para comprobar:

- Paginación.
- Consultas.
- Permisos.
- Restricción por organización.
- Exportación de información a Excel.

El comando utiliza `get_or_create`, por lo que si los registros de prueba ya existen no vuelve a duplicarlos.

El comando también crea, cuando sea necesario, la zona, el producto y el dispositivo utilizados para generar los mantenimientos de prueba.

Los usuarios de demostración se configuran de forma independiente y no son creados actualmente por `seed_data`.

# 9. Ejecutar el proyecto

Ejecutar:

```bash
python manage.py runserver
```

Luego abrir:

```text
http://127.0.0.1:8000/
```

La aplicación principal de zonas se encuentra en:

```text
http://127.0.0.1:8000/zonas/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

---

# Usuarios y rutas para la evaluación

El proyecto utiliza tres usuarios de demostración para comprobar los diferentes niveles de acceso y permisos.

Estas credenciales corresponden exclusivamente al proyecto académico.

---

## 1. Administrador general

```text
Usuario: admin
Contraseña: EcoEnergy#2026Admin
```

Corresponde al superusuario y posee acceso completo al sistema.

### Rutas para probar

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

Aplicación principal:

```text
http://127.0.0.1:8000/zonas/
```

Organizaciones:

```text
http://127.0.0.1:8000/accounts/organizations/
```

Crear organización:

```text
http://127.0.0.1:8000/accounts/organizations/create/
```

Dispositivos instalados:

```text
http://127.0.0.1:8000/devices/
```

Crear dispositivo:

```text
http://127.0.0.1:8000/devices/create/
```

Zonas:

```text
http://127.0.0.1:8000/devices/zones/
```

Crear zona:

```text
http://127.0.0.1:8000/devices/zones/create/
```

Solicitudes de mantenimiento:

```text
http://127.0.0.1:8000/maintenance/
```

Crear mantenimiento:

```text
http://127.0.0.1:8000/maintenance/create/
```

Exportar mantenimientos a Excel:

```text
http://127.0.0.1:8000/maintenance/export/excel/
```

---

## 2. Administrador de organización

```text
Usuario: admin_organizacion
Contraseña: EcoEnergy#2026
```

Posee permisos administrativos sobre la información autorizada de su organización.

Los QuerySets y formularios restringen los datos disponibles según la organización asociada al usuario.

### Rutas para probar

Aplicación principal:

```text
http://127.0.0.1:8000/zonas/
```

Organizaciones:

```text
http://127.0.0.1:8000/accounts/organizations/
```

Dispositivos:

```text
http://127.0.0.1:8000/devices/
```

Crear dispositivo:

```text
http://127.0.0.1:8000/devices/create/
```

Zonas:

```text
http://127.0.0.1:8000/devices/zones/
```

Crear zona:

```text
http://127.0.0.1:8000/devices/zones/create/
```

Mantenimientos:

```text
http://127.0.0.1:8000/maintenance/
```

Crear mantenimiento:

```text
http://127.0.0.1:8000/maintenance/create/
```

Exportar mantenimientos a Excel:

```text
http://127.0.0.1:8000/maintenance/export/excel/
```

Los registros disponibles para este usuario se encuentran restringidos a su organización.

---

## 3. Usuario de consulta

```text
Usuario: consulta
Contraseña: EcoEnergy#2026
```

Posee permisos limitados de consulta.

### Rutas para probar

Aplicación principal:

```text
http://127.0.0.1:8000/zonas/
```

Solicitudes de mantenimiento:

```text
http://127.0.0.1:8000/maintenance/
```

Exportar mantenimientos a Excel:

```text
http://127.0.0.1:8000/maintenance/export/excel/
```

En solicitudes de mantenimiento puede visualizar los registros autorizados y utilizar la exportación a Excel.

No puede crear, editar ni eliminar solicitudes de mantenimiento.

Si intenta acceder directamente a una operación para la cual no posee permiso, el sistema rechaza el acceso.

---

# Recuperación de contraseña

La recuperación se encuentra disponible en:

```text
http://127.0.0.1:8000/accounts/password-reset/
```

El proceso consiste en:

1. Ingresar el correo registrado.
2. Generar un código aleatorio de 6 dígitos.
3. Enviar el código al correo electrónico.
4. Verificar el código ingresado.
5. Validar su tiempo de expiración.
6. Establecer una nueva contraseña.
7. Invalidar el código utilizado.

El sistema también controla intentos fallidos y requisitos mínimos de seguridad de la nueva contraseña.

---

# CRUD implementados

El proyecto posee cuatro CRUD principales desarrollados para la aplicación.

## Organizaciones

Permite:

- Crear.
- Listar.
- Editar.
- Eliminar lógicamente.

Ruta:

```text
/accounts/organizations/
```

## Dispositivos instalados

Permite:

- Crear.
- Listar.
- Editar.
- Eliminar lógicamente.
- Cargar imágenes.

Ruta:

```text
/devices/
```

## Zonas

Permite:

- Crear.
- Listar.
- Editar.
- Eliminar lógicamente.

Ruta:

```text
/devices/zones/
```

## Solicitudes de mantenimiento

Permite:

- Crear.
- Listar.
- Editar.
- Eliminar lógicamente.
- Paginar registros.
- Exportar información a Excel.

Ruta:

```text
/maintenance/
```

---

# Funcionalidades implementadas

El sistema incluye:

- Inicio de sesión.
- Cierre de sesión.
- Recuperación de contraseña.
- Código de recuperación de 6 dígitos.
- Envío de correo mediante SMTP.
- Usuarios y perfiles.
- Grupos y permisos.
- Restricción de información por organización.
- CRUD de organizaciones.
- CRUD de zonas.
- CRUD de dispositivos instalados.
- CRUD de solicitudes de mantenimiento.
- Gestión de departamentos.
- Catálogo de dispositivos.
- Mediciones de energía.
- Eliminación lógica.
- Validaciones del lado del servidor.
- Django Forms y ModelForm.
- Carga de imágenes.
- Validación de imágenes mediante Pillow.
- Paginación.
- Persistencia de registros por página mediante sesión.
- SweetAlert2 para confirmaciones.
- Exportación Excel.
- Django Admin.
- Datos de prueba reproducibles.

---

# Eliminación lógica

Las entidades que requieren eliminación lógica utilizan:

```text
deleted_at
```

Los registros no son eliminados físicamente durante el flujo normal de la aplicación.

Al eliminar un registro se establece su fecha de eliminación y deja de aparecer en los listados activos.

---

# Seguridad y permisos

Las vistas protegidas requieren autenticación y los permisos correspondientes.

El sistema utiliza permisos de Django para controlar operaciones como:

- Visualizar.
- Crear.
- Modificar.
- Eliminar.

Además, los usuarios que no son superusuarios tienen restringida la información según su organización.

Por ejemplo, `admin_organizacion` solamente puede trabajar con los registros autorizados pertenecientes a su organización.

El usuario `consulta` posee permisos limitados de visualización.

---

# Imágenes de dispositivos

Los dispositivos instalados permiten cargar imágenes.

El sistema valida:

- JPG.
- JPEG.
- PNG.
- Tamaño máximo de 5 MB.
- Contenido real de la imagen mediante Pillow.

Los archivos cargados por los usuarios se almacenan en:

```text
media/
```

La carpeta `media/` no se versiona en GitHub.

---

# Paginación

El listado de solicitudes de mantenimiento permite seleccionar:

```text
5
15
30
```

registros por página.

La selección realizada por el usuario se conserva mediante la sesión.

---

# Exportación Excel

Las solicitudes de mantenimiento pueden exportarse en formato:

```text
.xlsx
```

La funcionalidad utiliza `openpyxl`.

La exportación respeta:

- Los permisos del usuario.
- La organización correspondiente.
- Los registros activos.
- La eliminación lógica.

Ruta:

```text
http://127.0.0.1:8000/maintenance/export/excel/
```

---

# Base de datos

El proyecto utiliza MariaDB.

La configuración de conexión se obtiene desde variables de entorno.

Las tablas del sistema son creadas mediante las migraciones de Django:

```bash
python manage.py migrate
```

Esto permite reconstruir la estructura de la base de datos en otro computador sin copiar manualmente la base utilizada durante el desarrollo.

---

# Archivos que no se suben a GitHub

El proyecto utiliza `.gitignore` para evitar versionar archivos privados o generados localmente.

Entre ellos:

```text
.env
db.sqlite3
db.sqlite3-journal
media/
.venv/
venv/
env/
__pycache__/
datos_ecoenergy.json
datos_ecoenergy_utf8.json
datos_ecoenergy_corregido.json
```

El archivo:

```text
.env.example
```

sí debe mantenerse en GitHub porque sirve como referencia para configurar el proyecto en otro computador.

---

# Comandos principales

Comprobar el proyecto:

```bash
python manage.py check
```

Aplicar migraciones:

```bash
python manage.py migrate
```

Mostrar migraciones:

```bash
python manage.py showmigrations
```

Generar datos de prueba:

```bash
python manage.py seed_data
```

Ejecutar el servidor:

```bash
python manage.py runserver
```

---

# Tecnologías utilizadas

- Python
- Django 6.1
- MariaDB
- mysqlclient
- python-dotenv
- Pillow
- openpyxl
- Bootstrap
- SweetAlert2
- Git
- GitHub

---

# Instalación completa en otro computador

Para levantar el proyecto desde cero en otro computador:

## Paso 1 — Instalar programas necesarios

Instalar:

```text
Git
Python 3.12 o superior
MariaDB Server
```

## Paso 2 — Clonar el proyecto

Desde Git Bash:

```bash
git clone https://github.com/DiegoInd/Backend-Flex-EcoEnergy.git
cd Backend-Flex-EcoEnergy
```

## Paso 3 — Crear el entorno virtual

```bash
python -m venv .venv
source .venv/Scripts/activate
```

## Paso 4 — Instalar las dependencias

```bash
pip install -r requirements.txt
```

## Paso 5 — Crear la base de datos

En MariaDB crear:

```sql
CREATE DATABASE ecoenergy_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

## Paso 6 — Crear `.env`

Copiar la estructura de:

```text
.env.example
```

y crear:

```text
.env
```

Configurar principalmente:

```text
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
```

Si se utilizará recuperación de contraseña mediante correo real, también configurar las variables `EMAIL_*`.

## Paso 7 — Crear las tablas

```bash
python manage.py migrate
```

## Paso 8 — Generar datos de demostración

```bash
python manage.py seed_data
```

## Paso 9 — Verificar el proyecto

```bash
python manage.py check
```

Resultado esperado:

```text
System check identified no issues (0 silenced).
```

## Paso 10 — Ejecutar

```bash
python manage.py runserver
```

Abrir:

```text
http://127.0.0.1:8000/
```

Para probar directamente los módulos se pueden utilizar las rutas indicadas anteriormente para cada usuario.