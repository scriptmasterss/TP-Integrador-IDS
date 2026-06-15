"""Servicio de base de datos para reserva."""

import flask
import requests

from config import API_TIMEOUT, API_URL
from servicios.api import api, refrezcar_token

OBJETO = "reserva"
LIMITE_POR_DEFECTO = 10


def crear(nuevo_objeto):
    """Crea un nuevo objeto."""
    refrezcar_token()
    BASE_URL = f"{API_URL}/{OBJETO}"
    if flask.session.get("rol") in ["alumno", "profesor"]:
        BASE_URL += "/crear"

    try:
        respuesta = api.post(BASE_URL, timeout=API_TIMEOUT, json=nuevo_objeto)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API crear {OBJETO} falló con: {e}")
        return None, None


def leer_paginado(pagina=1, limite=LIMITE_POR_DEFECTO, offset=None, filtros={}):
    """Lee de forma paginada."""
    refrezcar_token()
    BASE_URL = f"{API_URL}/{OBJETO}"
    if flask.session.get("rol") in ["alumno", "profesor"]:
        BASE_URL += "/leer"

    if offset is None:
        offset = (pagina - 1) * limite

    parametros = {"pagina": pagina, "limite": limite, "offset": offset, **filtros}

    try:
        respuesta = api.get(BASE_URL, timeout=API_TIMEOUT, params=parametros)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API leer paginado {OBJETO} falló con: {e}")
        return None, None


def leer_uno(id):
    """Lee uno."""
    refrezcar_token()
    BASE_URL = f"{API_URL}/{OBJETO}"
    if flask.session.get("rol") in ["alumno", "profesor"]:
        BASE_URL += "/leer"

    try:
        respuesta = api.get(f"{BASE_URL}/{id}", timeout=API_TIMEOUT)
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
    BASE_URL = f"{API_URL}/{OBJETO}"
    if flask.session.get("rol") in ["alumno", "profesor"]:
        BASE_URL += "/eliminar"

    try:
        respuesta = api.delete(f"{BASE_URL}/{id}", timeout=API_TIMEOUT)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API eliminar {OBJETO} falló con: {e}")
        return None, None


def aprobar(id):
    """Aprueba una."""
    refrezcar_token()
    try:
        respuesta = api.put(f"{API_URL}/{OBJETO}/aprobar/{id}", timeout=API_TIMEOUT)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API aprobar {OBJETO} falló con: {e}")
        return None, None


def rechazar(id):
    """Rechaza una."""
    refrezcar_token()
    try:
        respuesta = api.put(f"{API_URL}/{OBJETO}/rechazar/{id}", timeout=API_TIMEOUT)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API rechazar {OBJETO} falló con: {e}")
        return None, None


def entregar(id):
    """Entrega una."""
    refrezcar_token()
    try:
        respuesta = api.put(f"{API_URL}/{OBJETO}/entregar/{id}", timeout=API_TIMEOUT)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API entregar {OBJETO} falló con: {e}")
        return None, None


def devolver(id):
    """Devuelve una."""
    refrezcar_token()
    try:
        respuesta = api.put(f"{API_URL}/{OBJETO}/devolver/{id}", timeout=API_TIMEOUT)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API devolver {OBJETO} falló con: {e}")
        return None, None


def leer_total_actuales_y_historicas(filtros={}):
    """Lee total actuales y historicas."""
    refrezcar_token()
    try:
        respuesta = api.get(f"{API_URL}/{OBJETO}/leer_total_actuales_y_historicas", timeout=API_TIMEOUT, params=filtros)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API leer_total_actuales_y_historicas {OBJETO} falló con: {e}")
        return None, None


def leer_historial(pagina=1, limite=LIMITE_POR_DEFECTO, offset=None, filtros={}):
    """Lee de forma paginada reservas historicas."""
    refrezcar_token()
    if offset is None:
        offset = (pagina - 1) * limite

    parametros = {"pagina": pagina, "limite": limite, "offset": offset, **filtros}

    try:
        respuesta = api.get(f"{API_URL}/{OBJETO}/leer_historial", timeout=API_TIMEOUT, params=parametros)
        return respuesta.json(), respuesta.status_code
    except requests.exceptions.JSONDecodeError:
        return None, respuesta.status_code
    except requests.exceptions.RequestException as e:
        print(f"API leer paginado {OBJETO} falló con: {e}")
        return None, None
