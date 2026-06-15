"""Servicio de base de datos para faq."""

import requests

from config import API_TIMEOUT, API_URL
from servicios.api import api, refrezcar_token

OBJETO = "faq"
LIMITE_POR_DEFECTO = 5


def crear(nuevo_objeto):
    """Crea un nuevo objeto."""
    refrezcar_token()
    try:
        respuesta = api.post(f"{API_URL}/{OBJETO}", timeout=API_TIMEOUT, json=nuevo_objeto)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API crear {OBJETO} falló con: {e}")
        return None, None


def leer_paginado(pagina=1, limite=LIMITE_POR_DEFECTO, offset=None, filtros={}):
    """Lee de forma paginada."""
    refrezcar_token()
    if offset is None:
        offset = (pagina - 1) * limite

    parametros = {"pagina": pagina, "limite": limite, "offset": offset, **filtros}

    try:
        respuesta = api.get(f"{API_URL}/{OBJETO}", timeout=API_TIMEOUT, params=parametros)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API leer paginado {OBJETO} falló con: {e}")
        return None, None


def leer_uno(id):
    """Lee uno."""
    refrezcar_token()
    try:
        respuesta = api.get(f"{API_URL}/{OBJETO}/{id}", timeout=API_TIMEOUT)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API leer uno {OBJETO} falló con: {e}")
        return None, None


def actualizar_uno(id, nuevo_objeto):
    """Actualiza uno."""
    refrezcar_token()
    try:
        respuesta = api.put(f"{API_URL}/{OBJETO}/{id}", timeout=API_TIMEOUT, json=nuevo_objeto)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API crear {OBJETO} falló con: {e}")
        return None, None


def eliminar_uno(id):
    """Elimina uno."""
    refrezcar_token()
    try:
        respuesta = api.delete(f"{API_URL}/{OBJETO}/{id}", timeout=API_TIMEOUT)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API crear {OBJETO} falló con: {e}")
        return None, None
