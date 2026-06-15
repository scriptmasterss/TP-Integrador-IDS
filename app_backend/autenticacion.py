"""Implemente funciones para el manejo de autenticación y permisos."""

from functools import wraps

import bcrypt
import jwt
from flask import request

import respuestas
from config import JWT_ALGORITMO, JWT_SECRETO

ENCONDING = "utf-8"
JWT_VALIDO = "jwt valido"
JWT_INVALIDO = "jwt invalido"
JWT_EXPIRADO = "jwt expirado"
TOKEN_EXTRAIDO = "token extraido"
TOKEN_INCORRECTO = "tipo de token invalido, no comienza con Bearer"
SIN_TOKEN = "no hay token en el header Authorization"
CONTRASENIA_INVALIDA = "no se pudo valida la contraseña"


def hashear_contrasenia(contrasenia):
    """Genera el hash de una contraseña usando bcrypt."""
    hash_bytes = bcrypt.hashpw(contrasenia.encode(ENCONDING), bcrypt.gensalt())

    return hash_bytes.decode(ENCONDING)


def validar_contrasenia(contrasenia, contrasenia_hash):
    """Verifica si una contraseña coincide con su hash."""
    try:
        return bcrypt.checkpw(contrasenia.encode(ENCONDING), contrasenia_hash.encode(ENCONDING))

    except (ValueError, TypeError):
        return None


def generar_token(**kwargs):
    """Genera un token JWT."""
    return jwt.encode(kwargs, JWT_SECRETO, algorithm=JWT_ALGORITMO)


def generar_token_de_autenticacion(id_usuario, rol):
    """Genera un token JWT con el ID de usuario y su rol."""
    contenido = {
        "id_usuario": id_usuario,
        "rol": rol,
    }
    return generar_token(**contenido)


def decodificar_token(token):
    """Decodifica y valida un token JWT."""
    try:
        return jwt.decode(token, JWT_SECRETO, algorithms=[JWT_ALGORITMO]), JWT_VALIDO

    except jwt.ExpiredSignatureError:
        return None, JWT_INVALIDO

    except jwt.InvalidTokenError:
        return None, JWT_EXPIRADO


def extraer_token(request):
    """Extrae el token JWT del header Authorization de la petición."""
    header = request.headers.get("Authorization", None)

    if header is None:
        return None, SIN_TOKEN

    if not header.startswith("Bearer "):
        return None, TOKEN_INCORRECTO

    return header[len("Bearer ") :].strip(), TOKEN_EXTRAIDO


def requiere_rol(roles_permitidos=["alumno", "profesor", "bibliotecario", "admin"]):
    """Decorador que protege una ruta requiriendo autenticación y un rol específico."""

    def wrapperGenerator(route):
        @wraps(route)
        def wrapper(*args, **kwargs):
            """Extrae, decodifica, y carga los datos del token de autorización."""
            token, error = extraer_token(request)

            if token is None:
                return respuestas.desautenticado(error)

            contenido, error = decodificar_token(token)

            if contenido is None:
                return respuestas.desautenticado(error)

            if contenido.get("rol") not in roles_permitidos:
                return respuestas.desautorizado(error)

            request.usuario = contenido

            return route(*args, **kwargs)

        return wrapper

    return wrapperGenerator
