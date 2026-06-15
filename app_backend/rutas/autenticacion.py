"""Implementa rutas de autenticación."""

from flask import Blueprint, request

import autenticacion
import respuestas
import servicios
import validadores
from database import obtener_conexion

OBJETO = "autenticacion"

COLUMNA_CONTRASENIA = "contrasenia_hash"

blueprint = Blueprint(OBJETO, __name__)


@blueprint.route("/iniciar_sesion", methods=["POST"])
def iniciar_sesion():
    """Responde a iniciar_sesion."""
    cuerpo = request.get_json()

    email, error = validadores.general.email(cuerpo.get("email"))
    if email is None:
        return respuestas.peticion_incorrecta(f"Email invalido, {error}")
    contrasenia, error = validadores.general.texto(cuerpo.get("contrasenia"))
    if contrasenia is None:
        return respuestas.peticion_incorrecta(f"contrasenia invalido, {error}")

    with obtener_conexion() as conexion:
        usuario, total, error = servicios.usuario.leer_paginado(conexion, filtros={"email": email})
        usuario = usuario[0] if total == 1 else None
        if usuario is None:
            if error == servicios.usuario.SIN_ERROR:
                return respuestas.no_encontrado(f"No se encontro usuario con email: {email}")
            else:
                return respuestas.error_interno(f"No logro iniciar sesion, {error}")

        if usuario.get("activo") == 0:
            return respuestas.peticion_incorrecta("Usuario desactivado")

        contrasenia_valida = autenticacion.validar_contrasenia(contrasenia, usuario.get(COLUMNA_CONTRASENIA))
        if contrasenia_valida is None:
            return respuestas.error_interno("No se logro validar la contraseña")

        if not contrasenia_valida:
            return respuestas.desautenticado("Contraseña incorrecta")

        id_usuario = usuario.get("id")
        rol = usuario.get("rol")
        token = autenticacion.generar_token_de_autenticacion(id_usuario, rol)

        respuesta = {
            "id_usuario": id_usuario,
            "rol": rol,
            "token": token,
        }

        return respuestas.correcto(respuesta)


@blueprint.route("/crear_cuenta", methods=["POST"])
def crear_cuenta():
    """Responde al crear cuenta."""
    nuevo_usuario, error = validadores.usuario.validar_nuevo(request.get_json())
    if nuevo_usuario is None:
        return respuestas.peticion_incorrecta(error)

    nuevo_usuario = {
        llave: valor for llave, valor in nuevo_usuario.items() if llave in validadores.usuario.LLAVES_OBLIGATORIAS
    }

    contrasenia = nuevo_usuario.pop("contrasenia")
    nuevo_usuario[COLUMNA_CONTRASENIA] = autenticacion.hashear_contrasenia(contrasenia)

    with obtener_conexion() as conexion:
        nuevo_usuario, error = servicios.usuario.crear(conexion, nuevo_usuario)
        if nuevo_usuario is None:
            if error == servicios.usuario.HUBO_CONFLICTO:
                return respuestas.conflico_de_datos(f"Ese usuario ya existe, {error}")
            else:
                return respuestas.error_interno(f"No se pudo crear el usuario, {error}")

        return respuestas.correcto(nuevo_usuario)


@blueprint.route("/sobre_mi", methods=["GET"])
@autenticacion.requiere_rol()
def sobre_mi():
    """Responde a sobre mi."""
    with obtener_conexion() as conexion:
        id_usuario = request.usuario.get("id_usuario")
        usuario, error = servicios.usuario.leer_uno(conexion, id_usuario)
        if usuario is None:
            if error == servicios.usuario.SIN_ERROR:
                return respuestas.no_encontrado("El usuario para este token, no existe")
            else:
                return respuestas.error_interno("No se pudo buscar el usuario")

        return respuestas.correcto(usuario)


@blueprint.route("/cambiar_contrasenia", methods=["POST"])
@autenticacion.requiere_rol()
def cambiar_contrasenia():
    """Responde a cambiar contrasenia."""
    id_usuario = request.usuario.get("id_usuario")
    nueva_contrasenia, error = validadores.general.contrasenia(request.get_json().get("nueva_contrasenia"))
    if nueva_contrasenia is None:
        return respuestas.peticion_incorrecta(error)

    nueva_contrasenia_hash = autenticacion.hashear_contrasenia(nueva_contrasenia)

    with obtener_conexion() as conexion:
        resultado, error = servicios.usuario.cambiar_contrasenia(conexion, id_usuario, nueva_contrasenia_hash)
        if resultado is None:
            if error == servicios.usuario.SIN_ERROR:
                return respuestas.no_encontrado("El usuario para este token, no existe")
            else:
                return respuestas.error_interno("No se pudo cambiar la contrasenia del el usuario")

        return respuestas.correcto(resultado)
