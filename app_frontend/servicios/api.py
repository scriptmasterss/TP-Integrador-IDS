"""Implementa la peticion de api."""

import requests
from flask import session

api = requests.Session()


def refrezcar_token():
    """Actualiza el token de las peticiones."""
    token = session.get("token") or None
    if token is None:
        api.headers.pop("Authorization", None)
    else:
        api.headers.update({"Authorization": f"Bearer {token}"})
