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

loans_bp = Blueprint("loans", __name__)

def format_loan(row):
    return {
        "loan_id": row.get("id"),
        "user_id": row.get("id_usuario"),
        "status": row.get("estado_reserva"),
        "article_id": row.get("id_reservado"),
        "createdAt": row.get("fecha_retiro"),
        "returnedAt": row.get("fecha_regreso")
    }

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

