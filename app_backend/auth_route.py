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

auth_bp = Blueprint("auth", __name__)

def format_auth(row):
    return {
        "id": row.get("id"),
        "nombre": row.get("nombre"),
        "mail": row.get("mail"),
        "rol": row.get("rol")
    }

@auth_bp.route("/api/auth/me", methods=["GET"])
def autenticacion_usuario():
    """Devuelve los datos del perfil y el rol del usuario autenticado"

    Returns:
        tuple: Respuesta JSON con los datos autenticados (id, nombre, mail y rol) y codigo http 200,
        en caso de no encontrar el usuario codigo http 404.
    """
    
    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    user_id = request.headers.get("X-User-Id")

    if not user_id:
        return jsonify({"error": MSG_BAD_REQUEST}), HTTP_BAD_REQUEST
    
    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT id, nombre, mail, rol FROM usuario WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Usuario no encontrado"}), HTTP_NOT_FOUND
        
        return jsonify(format_auth(user)), HTTP_OK

    except mysql.connector.Error:
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    except Exception:
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conexion.close()
        except Exception:
            pass
