"""Servicio de base de datos para reserva."""

import mysql.connector
from mysql.connector import errorcode

from config import FORMATO_FECHA, FORMATO_HORA

OBJETO = "reserva"
LIMITE_POR_DEFECTO = 10
HUBO_CONFLICTO = "hubo conflicto"
HUBO_FALLA = "hubo falla"
SIN_ERROR = "operación exitosa"

COLUMNA_ESTADO = "estado_reserva"


def crear(conexion, nuevo_objeto):
    """Crea un nuevo objeto."""
    if not nuevo_objeto:
        return None, HUBO_FALLA

    llaves = nuevo_objeto.keys()
    columnas = ", ".join(llaves)
    valores_sql = ", ".join([f"%({llave})s" for llave in llaves])

    query = f"INSERT INTO {OBJETO} ({columnas}) VALUES ({valores_sql})"

    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute(query, nuevo_objeto)
        conexion.commit()
        nuevo_objeto["id"] = cursor.lastrowid
        return nuevo_objeto, SIN_ERROR
    except mysql.connector.Error as error:
        conexion.rollback()
        print(f"Error en crear de {OBJETO}")
        if error.errno == errorcode.ER_DUP_ENTRY:
            return None, HUBO_CONFLICTO
        return None, HUBO_FALLA


def leer_paginado(conexion, pagina=1, limite=LIMITE_POR_DEFECTO, offset=None, filtros=None):
    """Lee de forma paginada."""
    if offset is None:
        offset = (pagina - 1) * limite

    clausula_where = ""
    if filtros is not None and filtros:
        if "id_usuario" in filtros:
            filtros[f"{OBJETO}.id_usuario"] = filtros.pop("id_usuario")
        condiciones = " AND ".join([f"{llave} = %({llave})s" for llave in filtros.keys()])
        clausula_where = f"WHERE {condiciones}"

    query = f"""
    SELECT
        {OBJETO}.id,
        {OBJETO}.id_usuario,
        {OBJETO}.estado_reserva,
        DATE_FORMAT({OBJETO}.fecha_retiro, '{FORMATO_FECHA}') as fecha_retiro,
        DATE_FORMAT({OBJETO}.fecha_regreso, '{FORMATO_FECHA}') as fecha_regreso,
        DATE_FORMAT({OBJETO}.fecha_retiro, '{FORMATO_HORA}') as hora_retiro,
        DATE_FORMAT({OBJETO}.fecha_regreso, '{FORMATO_HORA}') as hora_regreso,
        articulos.nombre,
        DATE_FORMAT(penalizacion.fecha_inicio, '{FORMATO_FECHA}') as fecha_inicio_penalizacion,
        DATE_FORMAT(penalizacion.fecha_fin, '{FORMATO_FECHA}') as fecha_fin_penalizacion,
        DATE_FORMAT(penalizacion.fecha_inicio, '{FORMATO_HORA}') as hora_inicio_penalizacion,
        DATE_FORMAT(penalizacion.fecha_fin, '{FORMATO_HORA}') as hora_fin_penalizacion,
        penalizacion.id as id_penalizacion,
        penalizacion.motivo as motivo_penalizacion,
        penalizacion.activa as penalizacion_activa,
        penalizacion.severidad as severidad_penalizacion
    FROM {OBJETO}
    LEFT JOIN articulos ON id_articulo = articulos.id
    LEFT JOIN penalizacion ON {OBJETO}.id = penalizacion.id_reserva
    {clausula_where}
    LIMIT %(limite)s
    OFFSET %(offset)s
    """

    valores = {"limite": limite, "offset": offset, **(filtros or {})}

    query_de_cuenta = f"""
    SELECT COUNT(*) as total FROM {OBJETO} {clausula_where}
    """

    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute(query_de_cuenta, valores)
            total = cursor.fetchone().get("total", 0)
            cursor.execute(query, valores)
            return cursor.fetchall(), total, SIN_ERROR
    except mysql.connector.Error:
        print(f"Error en leer_paginado de {OBJETO}")
        return None, 0, HUBO_FALLA


def leer_uno(conexion, id):
    """Lee uno."""
    query = f"""
    SELECT
        {OBJETO}.id,
        {OBJETO}.id_usuario,
        {OBJETO}.id_articulo,
        {OBJETO}.estado_reserva,
        DATE_FORMAT({OBJETO}.fecha_retiro, '{FORMATO_FECHA}') as fecha_retiro,
        DATE_FORMAT({OBJETO}.fecha_regreso, '{FORMATO_FECHA}') as fecha_regreso,
        DATE_FORMAT({OBJETO}.fecha_retiro, '{FORMATO_HORA}') as hora_retiro,
        DATE_FORMAT({OBJETO}.fecha_regreso, '{FORMATO_HORA}') as hora_regreso,
        articulos.nombre,
        DATE_FORMAT(penalizacion.fecha_inicio, '{FORMATO_FECHA}') as fecha_inicio_penalizacion,
        DATE_FORMAT(penalizacion.fecha_fin, '{FORMATO_FECHA}') as fecha_fin_penalizacion,
        DATE_FORMAT(penalizacion.fecha_inicio, '{FORMATO_HORA}') as hora_inicio_penalizacion,
        DATE_FORMAT(penalizacion.fecha_fin, '{FORMATO_HORA}') as hora_fin_penalizacion,
        penalizacion.id as id_penalizacion,
        penalizacion.motivo as motivo_penalizacion,
        penalizacion.activa as penalizacion_activa,
        penalizacion.severidad as severidad_penalizacion
    FROM {OBJETO}
    LEFT JOIN articulos ON id_articulo = articulos.id
    LEFT JOIN penalizacion ON {OBJETO}.id = penalizacion.id_reserva
    WHERE {OBJETO}.id = %(id)s
    LIMIT 1
    """
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute(query, {"id": id})
            return cursor.fetchone(), SIN_ERROR
    except mysql.connector.Error:
        print(f"Error en leer_uno de {OBJETO}")
        return None, HUBO_FALLA


def actualizar_uno(conexion, id, nuevo_objeto):
    """Actualiza uno."""
    if not nuevo_objeto:
        return None, HUBO_FALLA

    set_clause = ", ".join([f"{llave} = %({llave})s" for llave in nuevo_objeto.keys()])

    query = f"""
    UPDATE {OBJETO}
    SET {set_clause}
    WHERE id = %(id)s
    """

    valores = {**nuevo_objeto, "id": id}

    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute(query, valores)
        conexion.commit()
        return True, SIN_ERROR
    except mysql.connector.Error as error:
        conexion.rollback()
        print(f"Error en actualizar_uno de {OBJETO}")
        if error.errno == errorcode.ER_DUP_ENTRY:
            return None, HUBO_CONFLICTO
        return None, HUBO_FALLA


def eliminar_uno(conexion, id):
    """Elimina uno."""
    query = f"""
    DELETE FROM {OBJETO}
    WHERE id = %(id)s
    """
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute(query, {"id": id})
        conexion.commit()
        return True, SIN_ERROR
    except mysql.connector.Error:
        print(f"Error en eliminar_uno de {OBJETO}")
        conexion.rollback()
        return None, HUBO_FALLA


def aprobar(conexion, id):
    """Aprueba una."""
    valores = {COLUMNA_ESTADO: "aprobado"}
    return actualizar_uno(conexion, id, valores)


def rechazar(conexion, id):
    """Rechaza una."""
    valores = {COLUMNA_ESTADO: "rechazado"}
    return actualizar_uno(conexion, id, valores)


def entregar(conexion, id):
    """Entrega una."""
    valores = {COLUMNA_ESTADO: "entregado"}
    return actualizar_uno(conexion, id, valores)


def devolver(conexion, id):
    """Devuelve una."""
    valores = {COLUMNA_ESTADO: "devuelto"}
    return actualizar_uno(conexion, id, valores)


def leer_disponibilidad(conexion, reserva):
    """Devuelve la disponibilidad de un articulo en un rango horario."""
    query_stock = "SELECT stock FROM articulos WHERE id = %(id_articulo)s"

    query_reservas = """
    SELECT COUNT(*) as ocupado
    FROM reserva
    WHERE id_articulo = %(id_articulo)s
    AND estado_reserva NOT IN ('rechazado', 'devuelto')
    AND fecha_retiro < %(fecha_regreso)s
    AND fecha_regreso > %(fecha_retiro)s
    """

    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute(query_stock, reserva)
            resultado = cursor.fetchone()
            if resultado is None:
                return None, SIN_ERROR

            stock_total = resultado["stock"]

            cursor.execute(query_reservas, reserva)
            ocupado = cursor.fetchone()["ocupado"]

            disponible = max(0, stock_total - ocupado)
            return disponible, SIN_ERROR

    except mysql.connector.Error:
        print("Error en leer_disponibilidad")
        return None, HUBO_FALLA


def leer_total_actuales_y_historicas(conexion, filtros):
    """Devuelve el total de reservas actuales e historicas."""
    clausula_where = ""
    if filtros is not None and filtros:
        condiciones = " AND ".join([f"{llave} = %({llave})s" for llave in filtros.keys()])
        clausula_where = f"WHERE {condiciones}"

    query = f"""
    SELECT COUNT(id) as total, estado_reserva
    FROM reserva
    {clausula_where}
    GROUP BY estado_reserva
    """

    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute(query, filtros)
            totales = cursor.fetchall()

            total_actual = 0
            total_historicas = 0

            for total in totales:
                if total.get("estado_reserva") == "entregado":
                    total_historicas += total.get("total")
                else:
                    total_actual += total.get("total")

            respuesta = {"total_actual": total_actual, "total_historicas": total_historicas}

            return respuesta, SIN_ERROR

    except mysql.connector.Error:
        print("Error en leer_total_actuales_y_historicas")
        return None, HUBO_FALLA


def leer_historial(conexion, pagina=1, limite=LIMITE_POR_DEFECTO, offset=None, filtros=None):
    """Lee de forma paginada el historial."""
    if offset is None:
        offset = (pagina - 1) * limite

    clausula_where = f"WHERE {COLUMNA_ESTADO} in ('devuelto', 'rechazado')"
    if filtros is not None and filtros:
        if "id_usuario" in filtros:
            filtros[f"{OBJETO}.id_usuario"] = filtros.pop("id_usuario")
        condiciones = " AND ".join([f"{llave} = %({llave})s" for llave in filtros.keys()])
        clausula_where += f"AND {condiciones}"

    query = f"""
    SELECT
        {OBJETO}.id,
        {OBJETO}.id_usuario,
        {OBJETO}.id_articulo,
        {OBJETO}.estado_reserva,
        DATE_FORMAT({OBJETO}.fecha_retiro, '{FORMATO_FECHA}') as fecha_retiro,
        DATE_FORMAT({OBJETO}.fecha_regreso, '{FORMATO_FECHA}') as fecha_regreso,
        DATE_FORMAT({OBJETO}.fecha_retiro, '{FORMATO_HORA}') as hora_retiro,
        DATE_FORMAT({OBJETO}.fecha_regreso, '{FORMATO_HORA}') as hora_regreso,
        articulos.nombre,
        DATE_FORMAT(penalizacion.fecha_inicio, '{FORMATO_FECHA}') as fecha_inicio_penalizacion,
        DATE_FORMAT(penalizacion.fecha_fin, '{FORMATO_FECHA}') as fecha_fin_penalizacion,
        DATE_FORMAT(penalizacion.fecha_inicio, '{FORMATO_HORA}') as hora_inicio_penalizacion,
        DATE_FORMAT(penalizacion.fecha_fin, '{FORMATO_HORA}') as hora_fin_penalizacion,
        penalizacion.motivo as motivo_penalizacion,
        penalizacion.activa as penalizacion_activa,
        penalizacion.severidad as severidad_penalizacion
    FROM {OBJETO}
    LEFT JOIN articulos ON id_articulo = articulos.id
    LEFT JOIN penalizacion ON {OBJETO}.id = penalizacion.id_reserva
    {clausula_where}
    LIMIT %(limite)s
    OFFSET %(offset)s
    """

    valores = {"limite": limite, "offset": offset, **(filtros or {})}

    query_de_cuenta = f"""
    SELECT COUNT(*) as total FROM {OBJETO} {clausula_where}
    """

    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute(query_de_cuenta, valores)
            total = cursor.fetchone().get("total", 0)
            cursor.execute(query, valores)
            return cursor.fetchall(), total, SIN_ERROR
    except mysql.connector.Error:
        print(f"Error en leer_historial de {OBJETO}")
        return None, 0, HUBO_FALLA
