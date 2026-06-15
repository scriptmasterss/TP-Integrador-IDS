"""Implementa respuestas con codigo y mensaje generico."""

from flask import redirect, render_template, url_for

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

CORRECTO = HTTP_OK
CREADO = HTTP_CREATED
SIN_CONTENIDO = HTTP_NO_CONTENT
PETICION_INCORRECTA = HTTP_BAD_REQUEST
DESAUTENTICADO = HTTP_UNAUTHORIZED
DESAUTORIZADO = HTTP_FORBIDDEN
NO_ENCONTRADO = HTTP_NOT_FOUND
CONFLICTO_DE_DATOS = HTTP_CONFLICT
ERROR_INTERNO = HTTP_INTERNAL_SERVER_ERROR

def peticion_incorrecta(detalle=""):
    """Renderiza peticion_incorrecta."""
    return render_template("paginas/peticion_incorrecta.html", detalle=detalle)


def desautenticado():
    """Redirecciona a iniciar sesion."""
    return redirect(url_for("publico.iniciar_sesion"))


def desautorizado(detalle=""):
    """Renderiza desautorizado."""
    return render_template("paginas/desautorizado.html", detalle=detalle)
