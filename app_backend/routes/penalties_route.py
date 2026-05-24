import traceback

import mysql.connector
from flask import Blueprint, jsonify, request

from database import get_connection
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
from validators import valid_id, valid_penalty_patch

penalties_bp = Blueprint("penalties", __name__)


@penalties_bp.route("/api/penalties/<int:penalty_id>", methods=["PATCH"])
def patch_penalty(penalty_id):

    conn = get_connection()
    if conn is None:
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    if valid_id(penalty_id) is None:
        return jsonify({"error": MSG_BAD_REQUEST}), HTTP_BAD_REQUEST

    try:
        data = request.get_json()
    except Exception:
        data = None

    is_valid, error = valid_penalty_patch(data)
    if not is_valid:
        return jsonify({"error": MSG_BAD_REQUEST, "detail": error}), HTTP_BAD_REQUEST

    if "status" in data:
        data.update({"active": 1 if data.get("status") == "Active" else 0})
        data.pop("status")

    if "notes" in data:
        data.update({"reason": data.get("notes")})
        data.pop("notes")

    keysToUpdate = list(data.keys())

    set_parts = [f"{k} = %({k})s" for k in keysToUpdate]

    if not data.get("active", True):
        set_parts.append("end_date = NOW()")

    set_clause = ", ".join(set_parts)
    data.update({"penalty_id": penalty_id})

    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        sql = f"UPDATE penalties SET {set_clause} WHERE id = %(penalty_id)s"
        cursor.execute(sql, data)
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": MSG_NOT_FOUND}), HTTP_NOT_FOUND

        cursor.execute(
            "SELECT id, user_id, reason, start_date, end_date, active, severity FROM penalties WHERE id = %(penalty_id)s",
            {"penalty_id": penalty_id},
        )

        row = cursor.fetchone()

        if not row:
            return jsonify({"message": MSG_NOT_FOUND}), HTTP_NOT_FOUND

        response = {
            "id": row.get("id"),
            "userId": row.get("user_id"),
            "loanId": None,
            "reason": row.get("reason"),
            "status": "Active" if row.get("active") else "Resolved",
            "severity": row.get("severity"),
            "notes": row.get("reason"),
            "createdAt": (
                row.get("start_date").isoformat() if row.get("start_date") else None
            ),
            "resolvedAt": (
                row.get("end_date").isoformat() if row.get("end_date") else None
            ),
        }

        return jsonify(response), HTTP_OK

    except mysql.connector.Error:
        traceback.print_exc()
        return jsonify({"error": MSG_DB_CONNECTION_FAILED}), HTTP_INTERNAL_SERVER_ERROR

    except Exception:
        traceback.print_exc()
        return jsonify({"error": MSG_INTERNAL_SERVER_ERROR}), HTTP_INTERNAL_SERVER_ERROR

    finally:
        try:
            cursor.close()

        except Exception:
            pass

        try:
            conn.close()

        except Exception:
            pass
