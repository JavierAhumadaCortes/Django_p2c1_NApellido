El README.md inicial debería tener esta estructura:
# EcoEnergy Back End

## Descripción

EcoEnergy es una aplicación web desarrollada con Python y Django para
administrar dispositivos y monitorear su consumo energético.

## Requisitos

- Python 3.10 o superior
- Git
- Visual Studio Code

## Instalación

### 1. Clonar el repositorio

git clone URL_DEL_REPOSITORIO
cd NOMBRE_DEL_REPOSITORIO

### 2. Crear el entorno virtual

python -m venv .venv

### 3. Activar el entorno en Git Bash

source .venv/Scripts/activate

### 4. Instalar las dependencias

python -m pip install -r requirements.txt

## Verificación

python -c "import sys; print(sys.executable)"
python -m django --version
python -m pip check

## Estado actual

- Repositorio creado.
- Entorno virtual configurado.
- Django instalado.
- Dependencias registradas.

## Próximos pasos

- Crear el proyecto Django.
- Configurar URLs y Views.
- Incorporar Templates.
En esta clase el README debe quedar como una primera versión. En las próximas sesiones incorporarán la ejecución con manage.py, la estructura del proyecto, sus rutas y funcionalidades
