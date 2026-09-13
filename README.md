# Backend-Flex-EcoEnergy

## Descripción

EcoEnergy es una aplicación desarrollada con Django para administrar organizaciones, departamentos, zonas, dispositivos, mediciones de energía y solicitudes de mantenimiento.

El proyecto utiliza Django Admin como interfaz de administración y aplica permisos y restricciones de acceso según la organización del usuario.

---

## Requisitos

- Python 3.12 o superior
- Git
- pip

---

## 1. Clonar el repositorio

```bash
git clone https://github.com/DiegoInd/Backend-Flex-EcoEnergy.git
cd Backend-Flex-EcoEnergy
```

---

## 2. Crear entorno virtual

### Windows

```bash
python -m venv .venv
```

Activar:

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Configurar variables de entorno

Crear un archivo llamado:

```text
.env
```

Se puede utilizar `.env.example` como referencia.

Ejemplo:

```env
SECRET_KEY=django-insecure-ecoenergy-desarrollo
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

El archivo `.env` no debe subirse al repositorio.

---

## 5. Aplicar migraciones

```bash
python manage.py migrate
```

Comprobar que el proyecto no tenga errores:

```bash
python manage.py check
```

---

## 6. Cargar datos de prueba

El proyecto incluye un Management Command que genera automáticamente los datos necesarios para la demostración.

Ejecutar:

```bash
python manage.py seed_demo
```

Este comando crea organizaciones, departamentos, zonas, dispositivos, mediciones, mantenimientos, grupos, permisos y usuarios de prueba.

También genera información perteneciente a EcoEnergy Chile y EcoEnergy Norte para comprobar el scoping por organización.

---

## 7. Usuarios de prueba

### Administrador general

Usuario:

```text
admin_demo
```

Contraseña:

```text
EcoEnergy2026!
```

Tiene acceso administrativo completo.

### Administrador organizacional

Usuario:

```text
admin_organizacion
```

Contraseña:

```text
EcoEnergy2026!
```

Tiene permisos administrativos limitados a su organización, EcoEnergy Chile.

### Usuario de consulta

Usuario:

```text
consulta
```

Contraseña:

```text
EcoEnergy2026!
```

Tiene permisos de consulta sobre dispositivos y mediciones.

Estas cuentas son exclusivamente para demostración y evaluación.

---

## 8. Ejecutar servidor

```bash
python manage.py runserver
```

Ingresar a Django Admin desde:

```text
http://127.0.0.1:8000/admin/
```

---

## Funcionalidades implementadas

El sistema incluye:

- Gestión de organizaciones.
- Gestión de departamentos.
- Gestión de zonas.
- Catálogo de dispositivos.
- Dispositivos instalados.
- Mediciones de energía.
- Solicitudes de mantenimiento.
- Usuarios y perfiles.
- Grupos y permisos.
- Scoping de información por organización.
- Búsqueda, filtros y ordenamiento en Django Admin.
- Inline de mediciones dentro de dispositivos.
- Acción personalizada para cambiar el estado de dispositivos.
- Validación controlada entre departamento y organización.
- Datos de demostración reproducibles mediante `seed_demo`.

---

## Seguridad por organización

Los usuarios no superusuarios solamente pueden visualizar y administrar información correspondiente a su organización.

Por ejemplo, el usuario:

```text
admin_organizacion
```

pertenece a EcoEnergy Chile y no puede visualizar los dispositivos ni las mediciones pertenecientes a EcoEnergy Norte.

---

## Comandos principales

```bash
python manage.py check
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```