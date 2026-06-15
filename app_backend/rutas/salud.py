"""Rutas para verificar el estado del sistema."""

from flask import Blueprint

import respuestas
from database import obtener_conexion

blueprint = Blueprint("salud", __name__)


@blueprint.route("/salud", methods=["GET"])
def salud():
    """Retorna ok si hay conexión a la base de datos."""
    with obtener_conexion() as conexion:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT 1")
            return respuestas.correcto("ok")


@blueprint.route("/ping", methods=["GET"])
def ping():
    """Retorna pong."""
    return respuestas.correcto("pong")
