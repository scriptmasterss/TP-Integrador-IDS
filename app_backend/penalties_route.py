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

penalties_bp = Blueprint("penalties", __name__)

def format_penalty(row):
    return{
        "id": row.get("id"),
        "user_id": row.get("id_usuario"),
        "reason": row.get("motivo"),
        "status": "Activa" if row.get("activa") else "Levantada",
        "severity": row.get("severity"),
        "createdAt": row.get("fecha_inicio").isoformat() if row.get("fecha_inicio") else None,
        "resolvedAt": row.get("fecha_fin").isoformat() if row.get("fecha_fin") else None, 
    }

@penalties_bp.route("/api/penalties/<int:penalty_id>", methods=["PUT"])
def modificar_penalizacion(penalty_id):
    """Modifica o levanta una penalizacion cambiando todo su registro.

    Args: 
        penalty_id (int): Identificador de la penalizacion.

    Returns: 
        tuple: Respuesta JSON con la penalizacion modificada y codigo http 200 si fue exitoso,
        http 400 si no se encontraron los valores o http 404 si no se encontró la penalizacion.

    """
    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    data = request.get_json()
    values = ["id", "id_usuario", "motivo", "fecha_inicio", "fecha_fin"]

    if not data or any(not data.get(value) for value in values):
        return jsonify({"error": MSG_BAD_REQUEST}), HTTP_BAD_REQUEST

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)
        query = "UPDATE penalizacion SET id_usuario = %s, motivo = %s, activa = %s, severity = %s, fecha_inicio = %s, fecha_fin = %s WHERE id = %s"
        cursor.execute(query, (
            data.get("id_usuario"),
            data.get("motivo"),
            data.get("activa"),
            data.get("severity"),
            data.get("fecha_inicio"),
            data.get("fecha_fin"),
            penalty_id
        ))
        conexion.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": MSG_NOT_FOUND}), HTTP_NOT_FOUND
        
        cursor.execute("SELECT id, id_usuario, motivo, activa, severity, fecha_inicio, fecha_fin FROM penalizacion WHERE id = %s", (penalty_id,))
        row = cursor.fetchone()
        return jsonify(format_penalty(row)), HTTP_OK

    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conexion.close()
        except Exception:
            pass
