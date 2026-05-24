import mysql.connector
from flask import Blueprint, jsonify, request

from database import get_connection
from http_codes_and_messages import (
    HTTP_BAD_REQUEST,
    HTTP_CONFLICT,
    HTTP_CREATED,
    HTTP_INTERNAL_SERVER_ERROR,
    HTTP_NOT_FOUND,
    HTTP_OK,
    MSG_BAD_REQUEST,
    MSG_CONFLICT,
    MSG_DB_CONNECTION_FAILED,
    MSG_INTERNAL_SERVER_ERROR,
    MSG_NOT_FOUND,
)
from validators import valid_id, valid_user, valid_user_update

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/api/users/<int:user_id>/loans", methods=["GET"])
def get_user_loans(user_id):

    conn = get_connection()
    if conn is None:
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        sql_query = """
            SELECT r.id,
                   r.item_id,
                   a.name AS item_name,
                   r.status,
                   r.pickup_date,
                   r.return_date
            FROM reservations r
            LEFT JOIN items a ON r.item_id = a.id
            WHERE r.user_id = %(user_id)s
            ORDER BY r.pickup_date DESC
        """
        values = {"user_id": user_id}

        cursor.execute(sql_query, values)
        loans = cursor.fetchall()

        if len(loans) == 0:
            return (
                jsonify({"message": MSG_NOT_FOUND}),
                HTTP_NOT_FOUND,
            )

        return jsonify(loans), HTTP_OK

    except Exception:
        return (
            jsonify({"error": MSG_INTERNAL_SERVER_ERROR}),
            HTTP_INTERNAL_SERVER_ERROR,
        )

    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass


@usuarios_bp.route("/api/users", methods=["POST"])
def create_user():

    conn = get_connection()
    if conn is None:
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    try:
        data = request.get_json()
    except Exception:
        data = None

    if not data:
        return jsonify({"error": MSG_BAD_REQUEST}), HTTP_BAD_REQUEST

    is_valid, error = valid_user(data)
    if not is_valid:
        return jsonify({"error": MSG_BAD_REQUEST, "detail": error}), HTTP_BAD_REQUEST

    cursor = None

    try:
        cursor = conn.cursor()
        sql = "INSERT INTO users (name, email, score, role, major) VALUES (%(name)s, %(email)s, %(score)s, %(role)s, %(major)s)"
        values = {
            "name": data.get("name"),
            "email": data.get("email"),
            "score": data.get("score") if data.get("score") is not None else 0,
            "role": data.get("role"),
            "major": data.get("major"),
        }
        cursor.execute(sql, values)
        conn.commit()
        user_id = cursor.lastrowid

        user = {
            "id": user_id,
            "name": data.get("name"),
            "email": data.get("email"),
            "score": data.get("score") if data.get("score") is not None else 0,
            "role": data.get("role"),
            "major": data.get("major"),
        }

        return jsonify(user), HTTP_CREATED

    except mysql.connector.Error as err:
        try:
            if err.errno == 1062:
                return (
                    jsonify({"error": MSG_CONFLICT, "detail": "duplicate_entry"}),
                    HTTP_CONFLICT,
                )
        except Exception:
            pass
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


@usuarios_bp.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    conn = get_connection()
    if conn is None:
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    if valid_id(user_id) is None:
        return jsonify({"error": MSG_BAD_REQUEST}), HTTP_BAD_REQUEST

    try:
        data = request.get_json()

    except Exception:
        data = None

    is_valid, error = valid_user_update(data)
    if not is_valid:
        return jsonify({"error": MSG_BAD_REQUEST, "detail": error}), HTTP_BAD_REQUEST

    keysToUpdate = data.keys()

    set_clause = ", ".join([f"{f} = %({f})s" for f in keysToUpdate])
    data.update({"user_id": user_id})

    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        sql = f"UPDATE users SET {set_clause} WHERE id = %(user_id)s"
        cursor.execute(sql, data)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": MSG_NOT_FOUND}), HTTP_NOT_FOUND

        cursor.execute(
            "SELECT id, name, email, score, role, major FROM users WHERE id = %(user_id)s",
            {"user_id": user_id},
        )

        user = cursor.fetchone()

        return jsonify(user), HTTP_OK

    except mysql.connector.Error as err:
        try:
            if err.errno == 1062:
                return (
                    jsonify({"error": MSG_CONFLICT, "detail": "duplicate_entry"}),
                    HTTP_CONFLICT,
                )
        except Exception:
            pass
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
