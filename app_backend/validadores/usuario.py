"""validadores para usuario."""

import validadores.general

LLAVES_OBLIGATORIAS = ["nombre", "email", "contrasenia", "carrera"]

MAPA_VALIDADORES = {
    "nombre": validadores.general.nombre,
    "email": validadores.general.email,
    "puntaje": validadores.general.numero_positivo,
    "contrasenia": validadores.general.contrasenia,
    "carrera": validadores.general.texto,
    "activo": validadores.general.booleano,
    "rol": validadores.general.texto,
    "id": validadores.general.numero_positivo,
}

NO_ES_ROL_VALIDO = "valor no es alumno, profesor, bibliotecario, o admin"
ENUM_ROL = ["alumno", "profesor", "bibliotecario", "admin"]


def validar_existente(valor):
    """Valida los campos presentes en el diccionario según el mapa de validadores."""
    for llave in valor.keys():
        if llave in MAPA_VALIDADORES:
            validador = MAPA_VALIDADORES[llave]
            valor_llave, error = validador(valor.get(llave))

            if valor_llave is None:
                return None, f"valor de {llave} invalido pues {error}"

            valor[llave] = valor_llave

    llave = "rol"
    if llave in valor.keys():
        valor_llave = valor.get(llave)
        if valor_llave not in ENUM_ROL:
            return None, NO_ES_ROL_VALIDO

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
