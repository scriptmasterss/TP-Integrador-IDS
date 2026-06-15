"""Implementa autenticación."""

from functools import wraps

from flask import redirect, session, url_for

import respuestas


def requiere_rol(roles_permitidos=["alumno", "profesor", "bibliotecario", "admin"]):
    """Decorador que protege requiriendo autenticación y un rol específico."""

    def wrapperGenerator(route):
        @wraps(route)
        def wrapper(*args, **kwargs):
            """Extrae, decodifica, y carga los datos del token de autorización."""
            token = session.get("token")

            if token is None:
                session.clear()
                return respuestas.desautenticado()

            rol = session.get("rol")

            if rol is None:
                session.clear()
                return respuestas.desautenticado()

            if rol not in roles_permitidos:
                return respuestas.desautorizado()

            return route(*args, **kwargs)

        return wrapper

    return wrapperGenerator


def requiere_desautenticado():
    """Decorador que protege requiriendo desautenticado."""

    def wrapperGenerator(route):
        @wraps(route)
        def wrapper(*args, **kwargs):
            """Extrae el rol, y redirecciona acorde."""
            rol = session.get("rol")

            if rol == "admin":
                return redirect(url_for("admin.dashboard"))

            if rol == "bibliotecario":
                return redirect(url_for("bibliotecario.dashboard"))

            if rol == "profesor":
                return redirect(url_for("profesor.dashboard"))

            if rol is not None:
                return redirect(url_for("alumno.dashboard"))

            return route(*args, **kwargs)

        return wrapper

    return wrapperGenerator
