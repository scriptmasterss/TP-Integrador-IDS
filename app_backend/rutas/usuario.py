"""Implementa rutas para usuario."""

import math

from flask import Blueprint, request

import autenticacion
import respuestas
import servicios
import validadores
from database import obtener_conexion

OBJETO = "usuario"
LIMITE_POR_DEFECTO = 10

blueprint = Blueprint(OBJETO, __name__)


@blueprint.route("/", methods=["GET"])
@autenticacion.requiere_rol(["admin", "bibliotecario"])
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
        filtros, error = validadores.usuario.validar_filtro(filtros)
        if filtros is None:
            return respuestas.peticion_incorrecta(error)

        resultados, total, error = servicios.usuario.leer_paginado(conexion, pagina, limite, offset, filtros)
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
@autenticacion.requiere_rol(["admin", "bibliotecario"])
def get_uno(id):
    """Responde al GET /id."""
    with obtener_conexion() as conexion:
        resultado, error = servicios.usuario.leer_uno(conexion, id)
        if resultado is None:
            if error == servicios.usuario.SIN_ERROR:
                return respuestas.no_encontrado(f"No se encontro {OBJETO} con ese id")
            else:
                return respuestas.error_interno(f"Error en {OBJETO} al leer base de datos, {error}")

        return respuestas.correcto(resultado)


@blueprint.route("/", methods=["POST"])
@autenticacion.requiere_rol(["admin", "bibliotecario"])
def post():
    """Responde al POST."""
    with obtener_conexion() as conexion:
        nuevo_objeto, error = validadores.usuario.validar_nuevo(request.get_json())
        if nuevo_objeto is None:
            return respuestas.peticion_incorrecta(error)

        nuevo_objeto["contrasenia_hash"] = autenticacion.hashear_contrasenia(nuevo_objeto.pop("contrasenia"))

        resultado, error = servicios.usuario.crear(conexion, nuevo_objeto)
        if resultado is None:
            return respuestas.error_interno(f"Error en {OBJETO} al crear en base de datos, {error}")

        return respuestas.creado(resultado)


@blueprint.route("/<int:id>", methods=["PUT", "PATCH"])
@autenticacion.requiere_rol(["admin", "bibliotecario"])
def put(id):
    """Responde al PUT o PATCH."""
    with obtener_conexion() as conexion:
        nuevo_objeto, error = validadores.usuario.validar_existente(request.get_json())
        if nuevo_objeto is None:
            return respuestas.peticion_incorrecta(error)

        resultado, error = servicios.usuario.actualizar_uno(conexion, id, nuevo_objeto)
        if resultado is None:
            return respuestas.error_interno(f"Error en {OBJETO} al actualizar en base de datos, {error}")

        return respuestas.sin_contenido()


@blueprint.route("/<int:id>", methods=["DELETE"])
@autenticacion.requiere_rol(["admin", "bibliotecario"])
def delete(id):
    """Responde al DELETE."""
    with obtener_conexion() as conexion:
        resultado, error = servicios.usuario.eliminar_uno(conexion, id)
        if resultado is None:
            return respuestas.error_interno(f"Error en {OBJETO} al eliminar en base de datos, {error}")

        return respuestas.sin_contenido()
