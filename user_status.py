import mysql.connector
from flask import Blueprint, jsonify, request
from database import obtener_conexion

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_INTERNAL_SERVER_ERROR = 500
MSG_BAD_REQUEST = "Invalid request data"
MSG_NOT_FOUND = "Resource not found"
MSG_DB_CONECTION_FAILED = "Database conection failed"

user_status_bp = Blueprint("user_status", __name__)

@user_status_bp.route('/api/users/<int:id>/status', methods=['PATCH'])
def patch_user_status(id):
    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": MSG_DB_CONECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    data = request.get_json()

    if not data or 'estado_usuario' not in data:
        return jsonify({"error": MSG_BAD_REQUEST}), HTTP_BAD_REQUEST

    estado_actualizado = data.get("estado_usuario")
    estado_valido = ["activo", "inactivo"]

    if estado_actualizado not in estado_valido:
        return jsonify({"error": MSG_BAD_REQUEST}), HTTP_BAD_REQUEST

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)
        query = "UPDATE usuario SET estado_usuario = %s WHERE id = %s"
        cursor.execute(query, (estado_actualizado, id))
        conexion.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": MSG_NOT_FOUND}), HTTP_NOT_FOUND

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
    
