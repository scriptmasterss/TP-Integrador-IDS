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
MSG_INTERNAL_SERVER_ERROR = "internal server error ocurred"

auth_bp = Blueprint("auth", __name__)

def format_auth(row):
    return {
        "id": row.get("id"),
        "nombre": row.get("nombre"),
        "mail": row.get("mail"),
        "rol": row.get("rol")
    }

@auth_bp.route("/api/auth/me", methods=["GET"])
def auth_user():
    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": MSG_DB_CONECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    mail = request.args.get("mail")
    password = request.args.get("password")
    if not mail or not password:
        retun jsonify({"error": MSG_BAD_REQUEST}), HTTP_BAD_REQUEST

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT id, nombre, mail, rol FROM usuario WHERE id = %s"
        cursor.execute(query, (mail, password))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "Invalid mail or password"}), HTTP_NOT_FOUND
        return jsonify(format_auth(user)), HTTP_OK

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

