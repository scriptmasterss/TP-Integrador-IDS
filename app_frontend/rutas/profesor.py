"""Rutas del area de profesores."""

from datetime import datetime

from flask import Blueprint, redirect, render_template, request, session, url_for

import autenticacion
import respuestas
import servicios
import validadores

blueprint = Blueprint("profesor", __name__)


@blueprint.route("/perfil", methods=["GET"])
@autenticacion.requiere_rol(["profesor"])
def perfil():
    """Renderiza perfil."""
    respuesta, codigo = servicios.autenticacion.sobre_mi()

    if codigo != respuestas.CORRECTO:
        return render_template("paginas/profesor/perfil.html", error=respuesta.get("detalles"))

    return render_template("paginas/profesor/perfil.html", **respuesta, **request.args)


@blueprint.route("/dashboard", methods=["GET"])
@autenticacion.requiere_rol(["profesor"])
def dashboard():
    """Renderiza dashboard."""
    return redirect(url_for("profesor.perfil"))
    respuesta, codigo = servicios.reserva.leer_total_actuales_y_historicas()

    if codigo != respuestas.CORRECTO:
        return render_template("paginas/profesor/dashboard.html", error=respuesta.get("detalles"))

    return render_template("paginas/profesor/dashboard.html", **respuesta)


@blueprint.route("/cambiar_contrasena", methods=["POST"])
@autenticacion.requiere_rol(["profesor"])
def cambiar_contrasena():
    """Procesa cambiar_contrasenia."""
    nueva_contrasena, error = validadores.general.contrasenia(request.form.get("nueva_contrasena"))
    if nueva_contrasena is None:
        return redirect(url_for("profesor.perfil", error=error))

    respuesta, codigo = servicios.autenticacion.cambiar_contrasenia(nueva_contrasena)

    if codigo != respuestas.CORRECTO:
        return redirect(url_for("profesor.perfil", error=respuesta.get("detalles")))

    return redirect(url_for("profesor.perfil", exito="Nueva contraseña establesida"))


@blueprint.route("/historial", methods=["GET"])
@autenticacion.requiere_rol(["profesor"])
def historial():
    """Renderiza historial."""
    pagina = request.args.get("pagina", 1)
    limite = request.args.get("limite", servicios.reserva.LIMITE_POR_DEFECTO)
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
        if llave not in ["pagina", "limite", "offset", "error"] and request.args.get(llave) != ""
    }

    id_usuario = session.get("id_usuario")
    if "id_usuario" in filtros and filtros.get("id_usuario") != id_usuario:
        return respuestas.desautorizado("No puedes ver el historial de otros")

    filtros["id_usuario"] = id_usuario

    filtros, error = validadores.reserva.validar_filtro(filtros)
    if filtros is None:
        return render_template("paginas/profesor/historial.html", error=error)

    respuesta, codigo = servicios.reserva.leer_historial(pagina, limite, offset, filtros)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/profesor/historial.html", error=respuesta.get("detalles"), **filtros)

    return render_template("paginas/profesor/historial.html", **respuesta, **filtros)


@blueprint.route("/nueva_reserva", methods=["GET"])
@autenticacion.requiere_rol(["profesor"])
def nueva_reserva():
    """Renderiza nueva_reserva."""
    if "id_articulo" not in request.args:
        return redirect(url_for("publico.catalogo"))

    return render_template("paginas/profesor/nueva_reserva.html", **request.args)


@blueprint.route("/nueva_reserva", methods=["POST"])
@autenticacion.requiere_rol(["profesor"])
def nueva_reserva_post():
    """Procesa nueva_reserva."""
    fecha = request.form.get("fecha")
    hora_retiro = request.form.get("desde")
    hora_regreso = request.form.get("hasta")
    peticion = {
        "id_usuario": session.get("id_usuario"),
        "id_articulo": request.form.get("id_articulo"),
        "fecha_retiro": datetime.strptime(f"{fecha} {hora_retiro}", "%Y-%m-%d %H:%M"),
        "fecha_regreso": datetime.strptime(f"{fecha} {hora_regreso}", "%Y-%m-%d %H:%M"),
    }
    nueva_reserva, error = validadores.reserva.validar_nuevo(peticion)
    if nueva_reserva is None:
        return redirect(url_for("profesor.nueva_reserva", **request.form, error=error))

    respuesta, codigo = servicios.reserva.crear(nueva_reserva)
    if codigo != respuestas.CREADO:
        return redirect(url_for("profesor.nueva_reserva", **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("profesor.reserva_id", id=respuesta.get("datos").get("id")))


@blueprint.route("/reserva", methods=["GET"])
@autenticacion.requiere_rol(["profesor"])
def reserva():
    """Renderiza reserva."""
    pagina = request.args.get("pagina", 1)
    limite = request.args.get("limite", servicios.reserva.LIMITE_POR_DEFECTO)
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
        if llave not in ["pagina", "limite", "offset", "exito", "error"] and request.args.get(llave) != ""
    }

    id_usuario = session.get("id_usuario")
    if "id_usuario" in filtros and filtros.get("id_usuario") != id_usuario:
        return respuestas.desautorizado("No puedes ver el historial de otros")

    filtros["id_usuario"] = id_usuario

    filtros, error = validadores.reserva.validar_filtro(filtros)
    if filtros is None:
        return render_template("paginas/profesor/historial.html", error=error)

    respuesta, codigo = servicios.reserva.leer_paginado(pagina, limite, offset, filtros)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/profesor/reserva.html", error=respuesta.get("detalles"), **filtros)

    return render_template("paginas/profesor/reserva.html", **respuesta, **filtros)


@blueprint.route("/reserva/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["profesor"])
def reserva_id(id):
    """Renderiza reserva_id."""
    respuesta, codigo = servicios.reserva.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/profesor/reserva_id.html", error=respuesta.get("detalles"))

    qr_image = servicios.qr.generar_qr(url_for("publico.reserva_escaneo", id=id, _external=True))
    qr_src = f"data:[<mediatype>];base64,{qr_image}"

    return render_template("paginas/profesor/reserva_id.html", **respuesta, qr_src=qr_src)


@blueprint.route("/reserva/<int:id>/comprobante", methods=["GET"])
@autenticacion.requiere_rol(["profesor"])
def comprobante(id):
    """Renderiza el comprobante adecuado para el estado de la reserva."""
    return "En proceso"


@blueprint.route("/reserva/<int:id>/eliminar", methods=["POST"])
@autenticacion.requiere_rol(["profesor"])
def reserva_id_eliminar(id):
    """Procesa eliminar reserva."""
    respuesta, codigo = servicios.reserva.eliminar_uno(id)

    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("profesor.reserva", error=respuesta.get("detalles")))

    return redirect(url_for("profesor.reserva", exito=""))


@blueprint.route("/penalizacion", methods=["GET"])
@autenticacion.requiere_rol(["profesor"])
def penalizacion():
    """Renderiza penalizacion."""
    pagina = request.args.get("pagina", 1)
    limite = request.args.get("limite", servicios.reserva.LIMITE_POR_DEFECTO)
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
        if llave not in ["pagina", "limite", "offset", "error"] and request.args.get(llave) != ""
    }

    id_usuario = session.get("id_usuario")
    if "id_usuario" in filtros and filtros.get("id_usuario") != id_usuario:
        return respuestas.desautorizado("No puedes ver el historial de otros")

    filtros["id_usuario"] = id_usuario

    filtros, error = validadores.penalizacion.validar_filtro(filtros)
    if filtros is None:
        return render_template("paginas/profesor/historial.html", error=error)

    respuesta, codigo = servicios.penalizacion.leer_paginado(pagina, limite, offset, filtros)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/profesor/penalizacion.html", error=respuesta.get("detalles"), **filtros)

    return render_template("paginas/profesor/penalizacion.html", **respuesta, **filtros)
