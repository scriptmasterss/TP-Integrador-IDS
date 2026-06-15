"""Implementa autenticación."""

import requests

from config import API_TIMEOUT, API_URL
from servicios.api import api, refrezcar_token

OBJETO = "autenticacion"


def iniciar_sesion(email, contrasenia):
    """Inicia sesion."""
    refrezcar_token()
    cuerpo = {"email": email, "contrasenia": contrasenia}

    try:
        respuesta = api.post(f"{API_URL}/{OBJETO}/iniciar_sesion", timeout=API_TIMEOUT, json=cuerpo)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API iniciar_sesion {OBJETO} falló con: {e}")
        return None, None


def crear_cuenta(nombre, email, carrera, contrasenia):
    """Responde al crear cuenta."""
    refrezcar_token()
    cuerpo = {"nombre": nombre, "email": email, "carrera": carrera, "contrasenia": contrasenia}

    try:
        respuesta = api.post(f"{API_URL}/{OBJETO}/crear_cuenta", timeout=API_TIMEOUT, json=cuerpo)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API crear_cuenta {OBJETO} falló con: {e}")
        return None, None


def sobre_mi():
    """Responde a sobre mi."""
    refrezcar_token()
    try:
        respuesta = api.get(f"{API_URL}/{OBJETO}/sobre_mi", timeout=API_TIMEOUT)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API sobre_mi {OBJETO} falló con: {e}")
        return None, None


def cambiar_contrasenia(nueva_contrasenia):
    """Responde a cambiar contrasenia."""
    refrezcar_token()
    cuerpo = {"nueva_contrasenia": nueva_contrasenia}

    try:
        respuesta = api.post(f"{API_URL}/{OBJETO}/cambiar_contrasenia", timeout=API_TIMEOUT, json=cuerpo)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API sobre_mi {OBJETO} falló con: {e}")
        return None, None
