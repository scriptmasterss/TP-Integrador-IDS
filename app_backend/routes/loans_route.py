"""Rutas para los endpoints de préstamos."""

import mysql.connector
from flask import Blueprint, jsonify, request

from database import obtener_conexion
from http_codes_and_messages import (
    HTTP_BAD_REQUEST,
    HTTP_INTERNAL_SERVER_ERROR,
    HTTP_NOT_FOUND,
    HTTP_OK,
    MSG_BAD_REQUEST,
    MSG_DB_CONNECTION_FAILED,
    MSG_INTERNAL_SERVER_ERROR,
    MSG_NOT_FOUND,
)
from validators import valid_id, valid_loan_status_update

loans_bp = Blueprint("loans", __name__)


def format_loan(row):
    """Formatea una fila de préstamo de la base de datos como respuesta de la API.

    Convierte los campos de fecha a formato ISO 8601 cuando están presentes.

    Args:
        row (dict): Diccionario con los datos del préstamo obtenidos de la
            base de datos.

    Returns:
        dict: Diccionario formateado con los campos del préstamo para la respuesta.

    """
    return {
        "id": row.get("id"),
        "id_usuario": row.get("id_usuario"),
        "id_reservado": row.get("id_reservado"),
        "estado_reserva": row.get("estado_reserva"),
        "fecha_retiro": (
            row.get("fecha_retiro").isoformat() if row.get("fecha_retiro") else None
        ),
        "fecha_regreso": (
            row.get("fecha_regreso").isoformat() if row.get("fecha_regreso") else None
        ),
    }


@loans_bp.route("/api/loans/<int:loan_id>/status", methods=["PATCH"])
def patch_loan_status(loan_id):  # noqa: PLR0911
    """Actualiza el estado de un préstamo.

    Recibe el ID del préstamo como parámetro de ruta y el nuevo estado
    en el cuerpo de la petición como JSON.

    Args:
        loan_id (int): Identificador único del préstamo a actualizar.

    Returns:
        tuple: JSON con el préstamo actualizado y el código HTTP correspondiente.

    """
    if valid_id(loan_id) is None:
        return jsonify({"error": MSG_BAD_REQUEST}), HTTP_BAD_REQUEST

    try:
        data = request.get_json()
    except Exception:
        data = None

    is_valid, error = valid_loan_status_update(data)
    if not is_valid:
        return jsonify({"error": MSG_BAD_REQUEST, "detail": error}), HTTP_BAD_REQUEST

    conn = obtener_conexion()
    if conn is None:
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            UPDATE reserva
            SET estado_reserva = %(estado_reserva)s
            WHERE id = %(loan_id)s
            """,
            {
                "estado_reserva": data.get("estado_reserva"),
                "loan_id": loan_id,
            },
        )
        conn.commit()

        cursor.execute(
            """
            SELECT id,
                   id_usuario,
                   id_reservado,
                   estado_reserva,
                   fecha_retiro,
                   fecha_regreso
            FROM reserva
            WHERE id = %(loan_id)s
            """,
            {"loan_id": loan_id},
        )
        loan = cursor.fetchone()

        if not loan:
            return jsonify({"message": MSG_NOT_FOUND}), HTTP_NOT_FOUND

        return jsonify(format_loan(loan)), HTTP_OK

    except mysql.connector.Error:
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    except Exception:
        return jsonify({"error": MSG_INTERNAL_SERVER_ERROR}), HTTP_INTERNAL_SERVER_ERROR

    finally:
        try:
            if cursor:
                cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass



@loans_bp.route("/api/loans", methods=["GET"])
def listar_prestamos():
    """Lista todos los prestamos, en caso de que el usuario sea un alumno solo mostrará las propias.
    Podran ser filtrados por fechas y estado, en caso de bibliotecario/admin podra filtrar también por alumno.

    Returns:
        tuple: Respuesta JSON con la lista de todos los prestamos y codigo http 200,
        http 404 si no se encuentra el usuario.
    """

    conexion = obtener_conexion()
    if conexion is None:
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    user_id = request.headers.get("X-User-Id")
    
    estado_filtro = request.args.get("estado_reserva")
    fecha_retiro_filtro = request.args.get("fecha_retiro")
    fecha_regreso_filtro = request.args.get("fecha_regreso")

    try: 
        limit = int(request.args.get("_limit", 10))
        offset = int(request.args.get("_offset", 0))
    except ValueError:
        return jsonify({"error": MSG_BAD_REQUEST}), HTTP_BAD_REQUEST

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)
        query_role = "SELECT rol FROM usuario WHERE id = %s"
        cursor.execute(query_role, (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found or invalid session"}), HTTP_NOT_FOUND

        user_role = user["rol"]
    
        conditions = []
        params = []

        id_usuario_filtro = request.args.get("id_usuario")

        if user_role == "alumno":
            conditions.append("id_usuario = %s")
            params.append(user_id)
            id_usuario_filtro = user_id
        else:
            if id_usuario_filtro:
                conditions.append("id_usuario = %s")
                params.append(id_usuario_filtro)

        if estado_filtro:
            conditions.append("estado_reserva = %s")
            params.append(estado_filtro) 
        if fecha_retiro_filtro:
            conditions.append("fecha_retiro = %s")
            params.append(fecha_retiro_filtro)
        if fecha_regreso_filtro:
            conditions.append("fecha_regreso = %s")
            params.append(fecha_regreso_filtro)
        
        clause_where = " WHERE " + " AND ".join(conditions) if conditions else ""
        query_count = f"SELECT COUNT(*) AS total FROM reserva{clause_where}"
        cursor.execute(query_count, tuple(params))
        total = cursor.fetchone()["total"]

        query = f"""
            SELECT id, id_usuario, estado_reserva, id_reservado, fecha_retiro, fecha_regreso
            FROM reserva{clause_where}
            ORDER BY id
            LIMIT %s OFFSET %s
        """

        cursor.execute(query, tuple(params) + (limit, offset))
        loans_list = [format_loan(row) for row in cursor.fetchall()]

        base_url = request.base_url
        filters = ""
        if estado_filtro: filters += f"&estado={estado_filtro}"
        if fecha_retiro_filtro: filters += f"&fecha_retiro={fecha_retiro_filtro}"
        if fecha_regreso_filtro: filters += f"&fecha_regreso={fecha_regreso_filtro}"

        last_off = max(0, ((total - 1) // limit) * limit) if total > 0 else 0

        links = {
            "_first": {"href": f"{base_url}?{filters}_offset=0&__limit={limit}"},
            "_prev": {"href": f"{base_url}?{filters}_offset={max(0, offset - limit)}&_limit={limit}"} if offset > 0 else None,
            "_next": {"href": f"{base_url}?{filters}_offset={offset + limit}&_limit={limit}"} if (offset + limit) < total else None,
            "_last": {"href": f"{base_url}?{filters}_offset={last_off}&_limit={limit}"}
        }
                
        return jsonify({"reservas": loans_list, "_links": links}), HTTP_OK

    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conexion.close()
        except Exception:
            pass

