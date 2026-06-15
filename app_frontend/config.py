"""Configuración de la aplicación frontend.

Carga las variables de entorno desde un archivo .env y expone
los valores de configuración necesarios para la ejecución de la
aplicación Flask del frontend.
"""

import os

from dotenv import find_dotenv, load_dotenv

# Localiza y carga el archivo .env más cercano
env_path = find_dotenv()
if env_path:
    if not load_dotenv(env_path):
        print("Archivo .env vacio, usando valores por defecto")
else:
    print("Archivo .env no encontrado, usando valores por defecto", env_path)

# Expone valores de configuración comunes con valores por defecto razonables
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
HOST = os.environ.get("FRONTEND_HOST", "127.0.0.1")
PORT = int(os.environ.get("FRONTEND_PORT", "5000"))

API_HOST = os.environ.get("BACKEND_HOST", "127.0.0.1")
API_PORT = os.environ.get("BACKEND_PORT", "5001")
API_URL = f"http://{API_HOST}:{API_PORT}/api"

API_TIMEOUT = 5

# Ajustes de generación de códigos QR
QR_BORDE = int(os.environ.get("QR_BORDER", "4"))
QR_TAMANIO = int(os.environ.get("QR_TAMANIO", "10"))
