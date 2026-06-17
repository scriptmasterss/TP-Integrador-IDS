"""Rutas de la API crear y actualizar el estado_devuelto de una reserva."""

import mysql.connector
from flask import Blueprint, jsonify, request

from database import obtener_conexion
from http_codes_and_messages import (
    HTTP_BAD_REQUEST,
    HTTP_INTERNAL_SERVER_ERROR,
    HTTP_OK,
    MSG_BAD_REQUEST,
    MSG_DB_CONNECTION_FAILED,
    MSG_INTERNAL_SERVER_ERROR,
)
from routes.auth_route import requiere_auth
from validators import valid_condiciones, valid_id

estado_devuelto_bp = Blueprint("estado_devuelto", __name__)

@estado_devuelto_bp.route("/api/estado_devuelto/<int:id_reserva>", methods=["PUT"])
@requiere_auth(roles=["admin", "bibliotecario"])
def update_estado_devuelto(id_reserva):
    """Actualiza o Crea el estado_devuelto de una reserva

    Cambia o Crea el estado_devuelto de una reserva, puede ser:
        no_aplica
        bueno
        dañado
        perdido

    Args:
        id_reserva (int): Identificador de la reserva asociada.

    Returns:
        tuple: Respuesta JSON con los datos actualizados del estado_devuelto
            y código HTTP 200. Retorna 400 si los datos son inválidos,
            o 500 si hay error interno.

    Raises:
        mysql.connector.Error: Si ocurre un error de base de datos,
            incluyendo entradas duplicadas (errno 1062).

    """
    conn = obtener_conexion()
    if conn is None:
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    if valid_id(id_reserva) is None:
        return jsonify({"error": MSG_BAD_REQUEST}), HTTP_BAD_REQUEST

    try:
        data = request.get_json()

    except Exception:
        data = None

    is_valid, error = valid_condiciones(data)
    if not is_valid:
        return jsonify({"error": MSG_BAD_REQUEST, "detail": error}), HTTP_BAD_REQUEST

    data.update({"id_reserva": id_reserva})

    columnas = ", ".join(data.keys())
    insert_clause = ", ".join([f"%({f})s" for f in data.keys()])
    update_clause = ", ".join([f"{f} = VALUES({f})" for f in data.keys() if f != "id_reserva"])

    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        sql = f"""
            INSERT INTO estado_devuelto ({columnas}) 
            VALUES ({insert_clause})
            ON DUPLICATE KEY UPDATE {update_clause}
        """
        cursor.execute(sql, data)
        conn.commit()

        cursor.execute(
            """
            SELECT id, id_reserva, dias_retraso, condiciones
            FROM estado_devuelto
            WHERE id_reserva = %(id_reserva)s
            """,
            {"id_reserva": id_reserva},
        )

        estado_devuelto = cursor.fetchone()

        return jsonify(estado_devuelto), HTTP_OK

    except mysql.connector.Error as err:
        return jsonify({"error": MSG_INTERNAL_SERVER_ERROR}), HTTP_INTERNAL_SERVER_ERROR

    except Exception:
        return jsonify({"error": MSG_INTERNAL_SERVER_ERROR}), HTTP_INTERNAL_SERVER_ERROR

    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass
