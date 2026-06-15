"""validadores de tipos generales."""

import re

ES_BOOLEANO = "es un booleano"
ES_DICCIONARIO = "es un diccionario"
ES_LISTA = "es una lista"
ES_NUMERO = "es un numero"
ES_TEXTO = "es texto"
ES_TUPLA = "es una tupla"
NO_CONVERTIBLE_A_BOOLEANO = "no es convertible a booleano"
NO_CONVERTIBLE_A_FECHA = "no es convertible a fecha"
NO_CONVERTIBLE_A_NUMERO = "no es convertible a número"
NO_CONVERTIBLE_A_TEXTO = "no es convertible a texto"
NO_ES_EMAIL = "no es un email valido"
NO_ES_CONTRASENIA_VALIDA = (
    "no es una contrasenia valida, tiene que tener una minuscula, una mayuscula, un número, y un simbolo especial"
)
NO_EXISTE = "no existe"
NUMERO_NO_POSITIVO = "no es positivo"
TEXTO_MUY_CHICO = "no es del largo mínimo"

SIN_ERROR = None

LARGO_MINIMO_NOMBRE = 3
LARGO_MINIMO_CONTRASENIA = 8
CONTRASENIA_REGEXP = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).+$"
EMAIL_REGEXP = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def booleano(valor):
    """Valida y convierte el valor a booleano, excluyendo explícitamente textos y colecciones."""
    if valor is None:
        return None, NO_EXISTE

    if isinstance(valor, str):
        if valor == "True":
            return True, SIN_ERROR
        if valor == "False":
            return False, SIN_ERROR
        valor, _error = numero(valor)
        if valor is None:
            return None, ES_TEXTO

    if isinstance(valor, dict):
        return None, ES_DICCIONARIO

    if isinstance(valor, tuple):
        return None, ES_TUPLA

    if isinstance(valor, list):
        return None, ES_LISTA

    try:
        valor = bool(valor)
    except (ValueError, TypeError):
        return None, NO_CONVERTIBLE_A_BOOLEANO

    return valor, SIN_ERROR


def numero(valor):
    """Valida y convierte el valor a un número entero, bloqueando booleanos y colecciones."""
    if valor is None:
        return None, NO_EXISTE

    if isinstance(valor, bool):
        return None, ES_BOOLEANO

    if isinstance(valor, dict):
        return None, ES_DICCIONARIO

    if isinstance(valor, tuple):
        return None, ES_TUPLA

    if isinstance(valor, list):
        return None, ES_LISTA

    try:
        valor = int(valor)
    except (ValueError, TypeError):
        return None, NO_CONVERTIBLE_A_NUMERO

    return valor, SIN_ERROR


def numero_positivo(valor):
    """Valida que el valor sea un número entero y verifica que sea estrictamente mayor a cero."""
    valor, error = numero(valor)
    if valor is None:
        return None, error

    if valor <= 0:
        return None, NUMERO_NO_POSITIVO

    return valor, SIN_ERROR


def numero_positivo_con_cero(valor):
    """Valida que el valor sea un número entero y verifica que sea estrictamente mayor a cero."""
    valor, error = numero(valor)
    if valor is None:
        return None, error

    if valor < 0:
        return None, NUMERO_NO_POSITIVO

    return valor, SIN_ERROR


def texto(valor, largo_minimo=None):
    """Valida y convierte el valor a cadena de texto, comprobando opcionalmente un largo mínimo."""
    if valor is None:
        return None, NO_EXISTE

    if isinstance(valor, bool):
        return None, ES_BOOLEANO

    if isinstance(valor, dict):
        return None, ES_DICCIONARIO

    if isinstance(valor, tuple):
        return None, ES_TUPLA

    if isinstance(valor, list):
        return None, ES_LISTA

    try:
        valor = str(valor)
    except (ValueError, TypeError):
        return None, NO_CONVERTIBLE_A_TEXTO

    if largo_minimo is not None:
        if len(valor) < largo_minimo:
            return None, TEXTO_MUY_CHICO + str(largo_minimo)

    return valor, SIN_ERROR


def nombre(valor):
    """Valida y convierte el valor a nombre valido."""
    valor, error = texto(valor, LARGO_MINIMO_NOMBRE)
    if valor is None:
        return None, error

    return valor, SIN_ERROR


def contrasenia(valor):
    """Valida y convierte valor a contraseña valida."""
    valor, error = texto(valor, LARGO_MINIMO_CONTRASENIA)
    if valor is None:
        return None, error

    if re.match(CONTRASENIA_REGEXP, valor) is None:
        return None, NO_ES_CONTRASENIA_VALIDA

    return valor, SIN_ERROR


def email(valor):
    """Valida valor, comprobando que sea un email valido."""
    valor, error = texto(valor)
    if valor is None:
        return None, error

    if re.match(EMAIL_REGEXP, valor) is None:
        return None, NO_ES_EMAIL

    return valor, SIN_ERROR


def fecha(valor):
    """Valida el valor como texto representativo de una fecha."""
    valor, error = texto(valor)
    if valor is None:
        return None, error

    return valor, SIN_ERROR
