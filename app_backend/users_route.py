import mysql.connector
from flask import Blueprint, jsonify, request
from database import obtener_conexion

from http_codes_and_messages import (
    HTTP_OK,
    HTTP_BAD_REQUEST,
    HTTP_NOT_FOUND,
    HTTP_INTERNAL_SERVER_ERROR,
    HTTP_CONFLICT,
    HTTP_CREATED,
    MSG_BAD_REQUEST,
    MSG_NOT_FOUND,
    MSG_DB_CONNECTION_FAILED,
    MSG_INTERNAL_SERVER_ERROR,
    MSG_CONFLICT,
)

users_bp = Blueprint("users", __name__)

@users_bp.route("/api/users/<int:id_usuario>/status", methods=["PATCH"])
def actualizar_status(id_usuario):
    """Modifica el estado del usuario activando o desactivandolo.

    Args:
        id_usuario (int): Identificador del usuario a modificar.

    Returns:
        JSON con el id, mensaje de exito y el estado actualizado con codigo http 200,
        codigo http 400 si el estado no es valido.
    """

    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    data = request.get_json()

    if not data or "estado_usuario" not in data:
        return jsonify({"error": MSG_BAD_REQUEST}), HTTP_BAD_REQUEST

    estado_actualizado = data.get("estado_usuario")
    estado_valido = ["activo", "inactivo"]

    if estado_actualizado not in estado_valido:
        return jsonify({"error": MSG_BAD_REQUEST}), HTTP_BAD_REQUEST

    es_activo = True if estado_actualizado == "activo" else False

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        query_user = "SELECT id FROM usuario WHERE id = %s"
        cursor.execute(query_user, (id_usuario,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": MSG_NOT_FOUND}), HTTP_NOT_FOUND
        
        query = "UPDATE usuario SET activo = %s WHERE id = %s"
        cursor.execute(query, (es_activo, id_usuario))
        conexion.commit()

        return jsonify({
            "message": "Estado de usuario actualizado con exito",
            "id": id_usuario,
            "nuevo_estado": estado_actualizado
        }), HTTP_OK
    
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conexion.close()
        except Exception:
            pass
