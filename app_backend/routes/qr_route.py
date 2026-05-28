import base64
import io
import json

import qrcode
from flask import Blueprint, jsonify

from config import QR_BORDE, QR_TAMANIO
from database import obtener_conexion
from http_codes_and_messages import HTTP_NOT_FOUND, HTTP_OK

qr_bp = Blueprint("qr", __name__)


def generar_qr(datos):
    """Genera una imagen QR a partir de un string de datos.

    Args:
        datos (str): String no vacío con el contenido a codificar en el QR.

    Returns:
        str: String en base64 que representa la imagen PNG del QR.
    """

    codigo_qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=QR_TAMANIO,
        border=QR_BORDE,
    )
    codigo_qr.add_data(datos)
    codigo_qr.make(fit=True)

    imagen = codigo_qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")
    buffer.seek(0)

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def construir_contenido_qr(reserva):
    """Construye el contenido a codificar en el QR a partir de una reserva.

    Args:
        reserva (dict): Diccionario con las claves id, id_reservado, fecha_retiro, fecha_regreso.

    Returns:
        str: String JSON con los datos de la reserva sin información sensible.
    """

    datos_qr = {
        "id_reserva": reserva["id"],
        "id_articulo": reserva["id_reservado"],
        "fecha_retiro": str(reserva["fecha_retiro"]),
        "fecha_regreso": str(reserva["fecha_regreso"]),
    }
    return json.dumps(datos_qr)


def obtener_reserva_por_id(id_reserva):
    """Obtiene una reserva de la base de datos por su id.

    Args:
        id_reserva (int): Entero con el id de la reserva a buscar.

    Returns:
        dict: Diccionario con los datos de la reserva si existe, None si no se encuentra.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reserva WHERE id = %s", (id_reserva,))
    reserva = cursor.fetchone()
    cursor.close()
    conexion.close()
    return reserva


@qr_bp.route("/api/qr/loans/<int:id_reserva>", methods=["GET"])
def obtener_qr_reserva(id_reserva):
    """Genera y devuelve el QR correspondiente a una reserva.

    El request debe incluir un JWT válido en el header Authorization.

    Args:
        id_reserva (int): Entero correspondiente a una reserva existente.

    Returns:
        tuple: JSON con id_reserva y qrData (imagen en base64) y código 200,
               o error 404 si no existe la reserva.
    """

    reserva = obtener_reserva_por_id(id_reserva)

    if reserva is None:
        return jsonify({"error": "Reserva no encontrada"}), HTTP_NOT_FOUND

    contenido_qr = construir_contenido_qr(reserva)
    imagen_qr = generar_qr(contenido_qr)

    return jsonify({"id_reserva": id_reserva, "qrData": imagen_qr}), HTTP_OK
