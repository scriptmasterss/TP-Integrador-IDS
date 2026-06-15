"""Implementa rutas para normativa."""

import math

from flask import Blueprint, request

import autenticacion
import respuestas
import servicios
import validadores
from database import obtener_conexion

OBJETO = "normativa"
LIMITE_POR_DEFECTO = 10

blueprint = Blueprint(OBJETO, __name__)


@blueprint.route("/", methods=["GET"])
def get():
    """Responde al GET."""
    with obtener_conexion() as conexion:
        pagina = request.args.get("pagina", 1)
        limite = request.args.get("limite", LIMITE_POR_DEFECTO)
        offset = request.args.get("offset", None)

        if pagina is not None:
            pagina, error = validadores.general.numero_positivo(pagina)
            if pagina is None:
                return respuestas.peticion_incorrecta(error)

        if limite is not None:
            limite, error = validadores.general.numero_positivo(limite)
            if limite is None:
                return respuestas.peticion_incorrecta(error)

        if offset is not None:
            offset, error = validadores.general.numero(offset)
            if offset is None:
                return respuestas.peticion_incorrecta(error)

        filtros = {llave: valor for llave, valor in request.args.items() if llave not in ["pagina", "limite", "offset"]}
        filtros, error = validadores.normativa.validar_filtro(filtros)
        if filtros is None:
            return respuestas.peticion_incorrecta(error)

        resultados, total, error = servicios.normativa.leer_paginado(conexion, pagina, limite, offset, filtros)
        if resultados is None:
            return respuestas.error_interno(f"Error en {OBJETO} al leer base de datos, {error}")

        respuesta = {
            "pagina": pagina,
            "paginas_totales": math.ceil(total / limite),
            "limite": limite,
            "offset": offset,
            "datos": resultados,
        }

        return respuestas.correcto(**respuesta)


@blueprint.route("/<int:id>", methods=["GET"])
def get_uno(id):
    """Responde al GET /id."""
    with obtener_conexion() as conexion:
        resultado, error = servicios.normativa.leer_uno(conexion, id)
        if resultado is None:
            if error == servicios.normativa.SIN_ERROR:
                return respuestas.no_encontrado(f"No se encontro {OBJETO} con ese id")
            else:
                return respuestas.error_interno(f"Error en {OBJETO} al leer base de datos, {error}")

        return respuestas.correcto(resultado)


@blueprint.route("/", methods=["POST"])
@autenticacion.requiere_rol(["admin", "bibliotecario"])
def post():
    """Responde al POST."""
    with obtener_conexion() as conexion:
        nuevo_objeto, error = validadores.normativa.validar_nuevo(request.get_json())
        if nuevo_objeto is None:
            return respuestas.peticion_incorrecta(error)

        resultado, error = servicios.normativa.crear(conexion, nuevo_objeto)
        if resultado is None:
            return respuestas.error_interno(f"Error en {OBJETO} al crear en base de datos, {error}")

        return respuestas.creado(resultado)


@blueprint.route("/<int:id>", methods=["PUT", "PATCH"])
@autenticacion.requiere_rol(["admin", "bibliotecario"])
def put(id):
    """Responde al PUT o PATCH."""
    with obtener_conexion() as conexion:
        nuevo_objeto, error = validadores.normativa.validar_existente(request.get_json())
        if nuevo_objeto is None:
            return respuestas.peticion_incorrecta(error)

        resultado, error = servicios.normativa.actualizar_uno(conexion, id, nuevo_objeto)
        if resultado is None:
            return respuestas.error_interno(f"Error en {OBJETO} al actualizar en base de datos, {error}")

        return respuestas.sin_contenido()


@blueprint.route("/<int:id>", methods=["DELETE"])
@autenticacion.requiere_rol(["admin", "bibliotecario"])
def delete(id):
    """Responde al DELETE."""
    with obtener_conexion() as conexion:
        resultado, error = servicios.normativa.eliminar_uno(conexion, id)
        if resultado is None:
            return respuestas.error_interno(f"Error en {OBJETO} al eliminar en base de datos, {error}")

        return respuestas.sin_contenido()
