"""Rutas publicas del frontend."""

from flask import Blueprint, redirect, render_template, request, session, url_for

import autenticacion
import respuestas
import servicios
import validadores

blueprint = Blueprint("publico", __name__)


@blueprint.route("/", methods=["GET"])
def index():
    """Renderiza inicio."""
    return render_template("paginas/index.html")


@blueprint.route("/crear_cuenta", methods=["GET"])
@autenticacion.requiere_desautenticado()
def crear_cuenta():
    """Renderiza crear_cuenta."""
    return render_template("paginas/crear_cuenta.html", **request.args)


@blueprint.route("/crear_cuenta", methods=["POST"])
@autenticacion.requiere_desautenticado()
def crear_cuenta_post():
    """Procesa crear_cuenta."""
    nombre, error_nombre = validadores.general.nombre(request.form.get("nombre"))
    email, error_email = validadores.general.email(request.form.get("email"))
    carrera, error_carrera = validadores.general.texto(request.form.get("carrera"))
    contrasenia, error_contrasenia = validadores.general.contrasenia(request.form.get("contrasenia"))

    if None in [nombre, email, carrera, contrasenia]:
        errores = {
            "error_nombre": error_nombre,
            "error_email": error_email,
            "error_carrera": error_carrera,
            "error_contrasenia": error_contrasenia,
        }
        return redirect(url_for("publico.crear_cuenta", **errores))

    respuesta, codigo = servicios.autenticacion.crear_cuenta(nombre, email, carrera, contrasenia)

    if codigo != respuestas.CORRECTO:
        return redirect(url_for("publico.crear_cuenta", error=respuesta.get("detalles")))

    return redirect(url_for("publico.iniciar_sesion"))


@blueprint.route("/iniciar_sesion", methods=["GET"])
@autenticacion.requiere_desautenticado()
def iniciar_sesion():
    """Renderiza iniciar sesión."""
    return render_template("paginas/iniciar_sesion.html", **request.args)


@blueprint.route("/iniciar_sesion", methods=["POST"])
@autenticacion.requiere_desautenticado()
def iniciar_sesion_post():
    """Procesa login contra backend y guarda sesión local."""
    email, error_email = validadores.general.email(request.form.get("email"))
    contrasenia, error_contrasenia = validadores.general.texto(request.form.get("contrasenia"))

    if None in [email, contrasenia]:
        errores = {
            "error_email": error_email,
            "error_contrasenia": error_contrasenia,
        }
        return redirect(url_for("publico.iniciar_sesion", **errores))

    respuesta, codigo = servicios.autenticacion.iniciar_sesion(email, contrasenia)

    if codigo != respuestas.CORRECTO:
        return redirect(url_for("publico.iniciar_sesion", error=respuesta.get("detalles")))

    id_usuario = respuesta.get("datos").get("id_usuario")
    rol = respuesta.get("datos").get("rol")
    token = respuesta.get("datos").get("token")
    session["id_usuario"] = id_usuario
    session["rol"] = rol
    session["token"] = token

    if rol == "admin":
        return redirect(url_for("admin.dashboard"))

    if rol == "bibliotecario":
        return redirect(url_for("bibliotecario.dashboard"))

    if rol == "profesor":
        return redirect(url_for("profesor.dashboard"))

    if rol is not None:
        return redirect(url_for("alumno.dashboard"))

    return redirect(url_for("publico.iniciar_sesion"))


@blueprint.route("/cerrar_sesion", methods=["GET"])
@autenticacion.requiere_rol()
def cerrar_sesion():
    """Cierra la sesión del usuario y renderiza cerrar_sesion."""
    session.clear()
    return render_template("paginas/cerrar_sesion.html")


@blueprint.route("/reserva/<int:id>/escaneo", methods=["GET"])
@autenticacion.requiere_rol(["admin", "bibliotecario"])
def reserva_escaneo(id):
    """Escanea reserva, y actualiza su estado."""
    respuesta, codigo = servicios.reserva.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return redirect(url_for("admin.reserva_id", id=id, error=respuesta.get("detalles")))

    if respuesta.get("datos").get("estado_reserva") == "aprobado":
        respuesta, codigo = servicios.reserva.entregar(id)
        if codigo != respuestas.CORRECTO:
            return redirect(url_for("admin.reserva_id", id=id, error=respuesta.get("detalles")))

    if respuesta.get("datos").get("estado_reserva") == "entregado":
        respuesta, codigo = servicios.reserva.devolver(id)
        if codigo != respuestas.CORRECTO:
            return redirect(url_for("admin.reserva_id", id=id, error=respuesta.get("detalles")))

    return redirect(url_for("admin.reserva_id", id=id))


@blueprint.route("/normas", methods=["GET"])
def normas():
    """Renderiza normas."""
    pagina = request.args.get("pagina", 1)
    limite = request.args.get("limite", servicios.normativa.LIMITE_POR_DEFECTO)
    offset = request.args.get("offset", None)

    if pagina is not None:
        pagina, error = validadores.general.numero_positivo(pagina)
        if pagina is None:
            return respuestas.peticion_incorrecta(error)

    if limite is not None:
        limite, error = validadores.general.numero_positivo(limite)
        if limite is None:
            return respuestas.peticion_incorrecta(error)

    if offset is not None:
        offset, error = validadores.general.numero(offset)
        if offset is None:
            return respuestas.peticion_incorrecta(error)

    filtros = {}
    respuesta, codigo = servicios.normativa.leer_paginado(pagina, limite, offset, filtros)

    if codigo != respuestas.CORRECTO:
        return render_template("paginas/normas.html", error=respuesta.get("detalles"))

    return render_template("paginas/normas.html", **respuesta)


@blueprint.route("/catalogo", methods=["GET"])
def catalogo():
    """Renderiza catalogo."""
    pagina = request.args.get("pagina", 1)
    limite = request.args.get("limite", servicios.articulos.LIMITE_POR_DEFECTO)
    offset = request.args.get("offset", None)

    if pagina is not None:
        pagina, error = validadores.general.numero_positivo(pagina)
        if pagina is None:
            return respuestas.peticion_incorrecta(error)

    if limite is not None:
        limite, error = validadores.general.numero_positivo(limite)
        if limite is None:
            return respuestas.peticion_incorrecta(error)

    if offset is not None:
        offset, error = validadores.general.numero(offset)
        if offset is None:
            return respuestas.peticion_incorrecta(error)

    filtros = {
        llave: valor
        for llave, valor in request.args.items()
        if llave not in ["pagina", "limite", "offset", "error"] and valor != ""
    }
    filtros, error = validadores.articulos.validar_filtro(filtros)
    if filtros is None:
        return render_template("paginas/catalogo.html", error=error)

    respuesta, codigo = servicios.articulos.leer_paginado(pagina, limite, offset, filtros)

    if codigo != respuestas.CORRECTO:
        return render_template("paginas/catalogo.html", error=respuesta.get("detalles"))

    return render_template("paginas/catalogo.html", **respuesta)


@blueprint.route("/faq", methods=["GET"])
def faq():
    """Renderiza faq"""
    pagina = request.args.get("pagina", 1)
    limite = request.args.get("limite", servicios.faq.LIMITE_POR_DEFECTO)
    offset = request.args.get("offset", None)

    if pagina is not None:
        pagina, error = validadores.general.numero_positivo(pagina)
        if pagina is None:
            return respuestas.peticion_incorrecta(error)

    if limite is not None:
        limite, error = validadores.general.numero_positivo(limite)
        if limite is None:
            return respuestas.peticion_incorrecta(error)

    if offset is not None:
        offset, error = validadores.general.numero(offset)
        if offset is None:
            return respuestas.peticion_incorrecta(error)

    filtros = {}
    respuesta, codigo = servicios.faq.leer_paginado(pagina, limite, offset, filtros)

    if codigo != respuestas.CORRECTO:
        return render_template("paginas/faq.html", error=respuesta.get("detalles"))

    return render_template("paginas/faq.html", **respuesta)


@blueprint.route("/catalogo/<int:id_articulo>")
def catalogo_id(id_articulo):
    """Renderiza detalle_articulo."""
    respuesta, codigo = servicios.articulos.leer_uno(id_articulo)

    if codigo != respuestas.CORRECTO:
        return render_template("paginas/detalle_articulo.html", error=respuesta.get("detalles"))

    return render_template("public/article_details.html", **respuesta)
