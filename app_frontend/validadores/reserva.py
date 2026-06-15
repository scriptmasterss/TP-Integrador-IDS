"""validadores para reserva."""

import validadores.general

LLAVES_OBLIGATORIAS = ["id_usuario", "id_articulo", "fecha_retiro", "fecha_regreso"]

MAPA_VALIDADORES = {
    "id_usuario": validadores.general.numero_positivo,
    "id_articulo": validadores.general.numero_positivo,
    "estado_reserva": validadores.general.texto,
    "fecha_retiro": validadores.general.fecha,
    "fecha_regreso": validadores.general.fecha,
    "id": validadores.general.numero_positivo,
    "q": validadores.general.texto,
}

NO_ES_ESTADO_VALIDO = "valor no es pendiente, aprobado, rechazado, entregado, o devuelto"
ENUM_ESTADO = ["pendiente", "aprobado", "rechazado", "entregado", "devuelto"]


def validar_existente(valor):
    """Valida los campos presentes en el diccionario según el mapa de validadores."""
    for llave in valor.keys():
        if llave in MAPA_VALIDADORES:
            validador = MAPA_VALIDADORES[llave]
            valor_llave, error = validador(valor.get(llave))

            if valor_llave is None:
                return None, f"valor de {llave} invalido pues {error}"

            valor[llave] = valor_llave

    llave = "estado_reserva"
    if llave in valor.keys():
        valor_llave = valor.get(llave)
        if valor_llave not in ENUM_ESTADO:
            return None, NO_ES_ESTADO_VALIDO

        valor[llave] = valor_llave

    return valor, validadores.general.SIN_ERROR


def validar_filtro(valor):
    """Valida que los campos presentes en el diccionario estén en el mapa de validadores y que sean validos."""
    for llave in valor.keys():
        if llave not in MAPA_VALIDADORES:
            return None, f"la llave {llave} no es un filtro valido"

    valor, error = validar_existente(valor)
    if valor is None:
        return None, error

    return valor, validadores.general.SIN_ERROR


def validar_nuevo(valor):
    """Valida que estén las llaves obligatorias y que su contenido sea correcto."""
    for llave_req in LLAVES_OBLIGATORIAS:
        if llave_req not in valor:
            return None, f"Falta la llave obligatoria: {llave_req}"

    valor_validado, error = validar_existente(valor)
    if valor_validado is None:
        return None, f"valor invalido pues {error}"

    return valor_validado, validadores.general.SIN_ERROR


def validar_completo(valor):
    """Valida el objeto como nuevo y además verifica el ID si está presente."""
    valor_validado, error = validar_nuevo(valor)
    if valor_validado is None:
        return None, error

    llave = "id"
    if llave in valor_validado:
        valor_llave, error = validadores.general.numero_positivo(valor_validado.get(llave))
        if valor_llave is None:
            return None, f"valor de {llave} invalido pues {error}"
        valor_validado[llave] = valor_llave

    return valor_validado, validadores.general.SIN_ERROR
