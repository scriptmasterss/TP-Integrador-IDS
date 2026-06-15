"""Implementa respuestas con codigo y mensaje generico."""

from flask import jsonify

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_INTERNAL_SERVER_ERROR = 500

MSG_OK = "OK"
MSG_CREATED = "Created"
MSG_NO_CONTENT = "No Content"
MSG_BAD_REQUEST = "Bad Request"
MSG_UNAUTHORIZED = "Unauthorized"
MSG_FORBIDDEN = "Forbidden"
MSG_NOT_FOUND = "Not Found"
MSG_CONFLICT = "Conflict"
MSG_INTERNAL_SERVER_ERROR = "Internal Server Error"

DESC_OK = "Todo correcto"
DESC_CREATED = "Lo enviado vue creado correctamente"
DESC_NO_CONTENT = "El servidos no ha retornado nada"
DESC_BAD_REQUEST = "Su peticion fue incorrecta"
DESC_UNAUTHORIZED = "No se pudo validar su identidad"
DESC_FORBIDDEN = "No tiene permisos para acceder a este recurso"
DESC_NOT_FOUND = "No se encontro lo pedido"
DESC_CONFLICT = "Lo enviado entra en conflico con algo ya existente"
DESC_INTERNAL_SERVER_ERROR = "El servidor sufrió una falla técnica"


def correcto(datos, **kwargs):
    """Retorna la respuesta de correcto."""
    respuesta = {"mensaje": MSG_OK, "descripcion_corta": DESC_OK, "datos": datos, **kwargs}
    return jsonify(respuesta), HTTP_OK


def creado(datos):
    """Retorna la respuesta de creado."""
    respuesta = {
        "mensaje": MSG_CREATED,
        "descripcion_corta": DESC_CREATED,
        "datos": datos,
    }
    return jsonify(respuesta), HTTP_CREATED


def sin_contenido():
    """Retorna la respuesta de sin contenido."""
    respuesta = {
        "mensaje": MSG_NO_CONTENT,
        "descripcion_corta": DESC_NO_CONTENT,
    }
    return jsonify(respuesta), HTTP_NO_CONTENT


def peticion_incorrecta(detalles):
    """Retorna la respuesta de peticion incorrecta."""
    respuesta = {
        "mensaje": MSG_BAD_REQUEST,
        "descripcion_corta": DESC_BAD_REQUEST,
        "detalles": detalles,
    }
    return jsonify(respuesta), HTTP_BAD_REQUEST


def desautenticado(detalles):
    """Retorna la respuesta de desautenticado."""
    respuesta = {
        "mensaje": MSG_UNAUTHORIZED,
        "descripcion_corta": DESC_UNAUTHORIZED,
        "detalles": detalles,
    }
    return jsonify(respuesta), HTTP_UNAUTHORIZED


def desautorizado(detalles):
    """Retorna la respuesta de desautorizado."""
    respuesta = {
        "mensaje": MSG_FORBIDDEN,
        "descripcion_corta": DESC_FORBIDDEN,
        "detalles": detalles,
    }
    return jsonify(respuesta), HTTP_FORBIDDEN


def no_encontrado(detalles):
    """Retorna la respuesta de no encontrado."""
    respuesta = {
        "mensaje": MSG_NOT_FOUND,
        "descripcion_corta": DESC_NOT_FOUND,
        "detalles": detalles,
    }
    return jsonify(respuesta), HTTP_NOT_FOUND


def conflico_de_datos(detalles):
    """Retorna la respuesta de conflico de datos."""
    respuesta = {
        "mensaje": MSG_CONFLICT,
        "descripcion_corta": DESC_CONFLICT,
        "detalles": detalles,
    }
    return jsonify(respuesta), HTTP_CONFLICT


def error_interno(detalles):
    """Retorna la respuesta de error interno."""
    respuesta = {
        "mensaje": MSG_INTERNAL_SERVER_ERROR,
        "descripcion_corta": DESC_INTERNAL_SERVER_ERROR,
        "detalles": detalles,
    }
    return jsonify(respuesta), HTTP_INTERNAL_SERVER_ERROR
