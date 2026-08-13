Backend-Flex-EcoEnergy
Descripción y Objetivo
Este repositorio contiene el desarrollo del Back End para Flex-EcoEnergy, un proyecto que se encuentra en su fase inicial de configuración y estructuración. El objetivo principal de este componente es proveer la lógica de servidor, la gestión de datos y las APIs necesarias para soportar las funcionalidades ecológicas y energéticas del sistema utilizando Django.

Requisitos Previos
Asegúrate de contar con las siguientes herramientas instaladas en tu sistema antes de continuar:

Python (versión 3.12.3 recomendada)

Git

Clonación del Repositorio
Para clonar el proyecto en tu máquina local, abre tu terminal y ejecuta el siguiente comando:

Bash
git clone https://github.com/DiegoInd/Backend-Flex-EcoEnergy.git
cd Backend-Flex-EcoEnergy
Creación y Activación del Entorno Virtual (.venv)
Es una buena práctica aislar las dependencias del proyecto utilizando un entorno virtual.

En macOS y Linux:

Bash
python3 -m venv .venv
source .venv/bin/activate
En Windows (Command Prompt / PowerShell):

Bash
python -m venv .venv
.venv\Scripts\activate
Instalación de Dependencias
Una vez activado el entorno virtual, instala las dependencias del proyecto listadas en el archivo requirements.txt:

Bash
pip install -r requirements.txt
Comandos de Verificación
Para verificar que el entorno y el proyecto estén configurados correctamente, puedes ejecutar las siguientes comprobaciones de Django:

Bash
python manage.py check
Si deseas iniciar el servidor de desarrollo localmente para comprobar que todo arranca de forma adecuada:

Bash
python manage.py runserver
Estado Actual y Próximos Pasos
Estado actual: El proyecto se encuentra en su etapa inicial, enfocándose en la configuración base del entorno con Python 3.12.3 y la estructura inicial de Django.

Próximos pasos:

Definir los modelos de datos iniciales en las aplicaciones de Django.

Configurar la base de datos de desarrollo.

Implementar las primeras rutas y vistas del API o sistema.# Backend-Flex-EcoEnergy