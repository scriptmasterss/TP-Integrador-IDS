"""Servicio de base de datos para usuario."""

import mysql.connector
from mysql.connector import errorcode

OBJETO = "usuario"
LIMITE_POR_DEFECTO = 10
HUBO_CONFLICTO = "hubo conflicto"
HUBO_FALLA = "hubo falla"
SIN_ERROR = "operación exitosa"


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
        q = filtros.pop("q", None)

        condiciones = " AND ".join([f"{llave} = %({llave})s" for llave in filtros.keys()])

        if q is not None:
            if condiciones != "":
                condiciones += " AND "
            condiciones += f"""(
                {OBJETO}.id = %(q)s OR
                {OBJETO}.legajo = %(q)s OR
                {OBJETO}.nombre LIKE %(q_amplio)s OR
                {OBJETO}.email LIKE %(q_amplio)s OR
                {OBJETO}.carrera LIKE %(q_amplio)s
            )"""
            filtros["q"] = q
            filtros["q_amplio"] = f"%{q}%"

        clausula_where = f"WHERE {condiciones}"

    query = f"""
    SELECT * FROM {OBJETO}
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
        {OBJETO}.legajo,
        {OBJETO}.nombre,
        {OBJETO}.email,
        {OBJETO}.rol,
        {OBJETO}.carrera,
        {OBJETO}.activo
    FROM {OBJETO}
    WHERE id = %(id)s
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


def cambiar_contrasenia(conexion, id, nueva_contrasenia_hash):
    """Cambia contrasenia."""
    return actualizar_uno(conexion, id, {"contrasenia_hash": nueva_contrasenia_hash})
