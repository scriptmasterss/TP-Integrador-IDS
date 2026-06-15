"""Rutas del area de administradores."""

from flask import Blueprint, redirect, render_template, request, url_for

import autenticacion
import respuestas
import servicios
import validadores

blueprint = Blueprint("admin", __name__)


@blueprint.route("/perfil", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def perfil():
    """Renderiza perfil."""
    respuesta, codigo = servicios.autenticacion.sobre_mi()

    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/perfil.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/perfil.html", **respuesta, **request.args)


@blueprint.route("/dashboard", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def dashboard():
    """Renderiza dashboard."""
    return redirect(url_for("admin.perfil"))
    return render_template("paginas/admin/dashboard.html")


@blueprint.route("/cambiar_contrasena", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def cambiar_contrasena():
    """Procesa cambiar_contrasenia."""
    nueva_contrasena, error = validadores.general.contrasenia(request.form.get("nueva_contrasena"))
    if nueva_contrasena is None:
        return redirect(url_for("admin.perfil", error=error))

    respuesta, codigo = servicios.autenticacion.cambiar_contrasenia(nueva_contrasena)

    if codigo != respuestas.CORRECTO:
        return redirect(url_for("admin.perfil", error=respuesta.get("detalles")))

    return redirect(url_for("admin.perfil", exito="Nueva contraseña establesida"))


@blueprint.route("/articulos", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def articulos():
    """Renderiza articulo."""
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
        if llave not in ["pagina", "limite", "offset", "error"] and request.args.get(llave) != ""
    }
    filtros, error = validadores.articulos.validar_filtro(filtros)
    if filtros is None:
        return render_template("paginas/admin/articulos.html", error=error)

    respuesta, codigo = servicios.articulos.leer_paginado(pagina, limite, offset, filtros)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/articulos.html", error=respuesta.get("detalles"), **filtros)

    return render_template("paginas/admin/articulos.html", **respuesta, **filtros)


@blueprint.route("/articulo/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def articulo_id(id):
    """Renderiza articulo_id."""
    respuesta, codigo = servicios.articulos.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/articulo_id.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/articulo_id.html", **respuesta)


@blueprint.route("/nuevo_articulo", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def nuevo_articulo():
    """Renderiza nuevo_articulo."""
    return render_template("paginas/admin/nuevo_articulo.html", **request.args)


@blueprint.route("/nuevo_articulo", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def nuevo_articulo_post():
    """Procesa nuevo_articulo."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nuevo_articulo, error = validadores.articulos.validar_nuevo(cuerpo)
    if nuevo_articulo is None:
        return redirect(url_for("admin.nuevo_articulo", **request.form, error=error))

    respuesta, codigo = servicios.articulos.crear(nuevo_articulo)
    if codigo != respuestas.CORRECTO:
        return redirect(url_for("admin.nuevo_articulo", **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("admin.articulo_id", id=respuesta.get("datos").get("id")))


@blueprint.route("/editar_articulo/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def editar_articulo(id):
    """Renderiza editar_articulo."""
    respuesta, codigo = servicios.articulos.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/editar_articulo.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/editar_articulo.html", **respuesta, **request.args)


@blueprint.route("/editar_articulo/<int:id>", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def articulo_id_editar(id):
    """Procesa editar_articulo."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nuevo_articulo, error = validadores.articulos.validar_nuevo(cuerpo)
    if nuevo_articulo is None:
        return redirect(url_for("admin.editar_articulo", id=id, **request.form, error=error))

    respuesta, codigo = servicios.articulos.actualizar_uno(id, nuevo_articulo)
    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.editar_articulo", id=id, **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("admin.editar_articulo", id=id, exito="Edicion Exitosa"))


@blueprint.route("/articulo/<int:id>/eliminar", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def articulo_id_eliminar(id):
    """Procesa eliminar articulo."""
    respuesta, codigo = servicios.articulos.eliminar_uno(id)

    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.articulos", error=respuesta.get("detalles")))

    return redirect(url_for("admin.articulos", exito=""))


@blueprint.route("/estado_devuelto", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def estado_devuelto():
    """Renderiza estado_devuelto."""
    pagina = request.args.get("pagina", 1)
    limite = request.args.get("limite", servicios.estado_devuelto.LIMITE_POR_DEFECTO)
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
    filtros, error = validadores.estado_devuelto.validar_filtro(filtros)
    if filtros is None:
        return render_template("paginas/admin/estado_devuelto.html", error=error)

    respuesta, codigo = servicios.estado_devuelto.leer_paginado(pagina, limite, offset, filtros)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/estado_devuelto.html", error=respuesta.get("detalles"), **filtros)

    return render_template("paginas/admin/estado_devuelto.html", **respuesta, **filtros)


@blueprint.route("/estado_devuelto/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def estado_devuelto_id(id):
    """Renderiza estado_devuelto_id."""
    respuesta, codigo = servicios.estado_devuelto.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/estado_devuelto_id.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/estado_devuelto_id.html", **respuesta)


@blueprint.route("/nuevo_estado_devuelto", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def nuevo_estado_devuelto():
    """Renderiza nuevo_estado_devuelto."""
    return render_template("paginas/admin/nuevo_estado_devuelto.html", **request.args)


@blueprint.route("/nuevo_estado_devuelto", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def nuevo_estado_devuelto_post():
    """Procesa nuevo_estado_devuelto."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nuevo_estado_devuelto, error = validadores.estado_devuelto.validar_nuevo(cuerpo)
    if nuevo_estado_devuelto is None:
        return redirect(url_for("admin.nuevo_estado_devuelto", **request.form, error=error))

    respuesta, codigo = servicios.estado_devuelto.crear(nuevo_estado_devuelto)
    if codigo != respuestas.CORRECTO:
        return redirect(url_for("admin.nuevo_estado_devuelto", **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("admin.estado_devuelto_id", id=respuesta.get("datos").get("id")))


@blueprint.route("/editar_estado_devuelto/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def editar_estado_devuelto(id):
    """Renderiza editar_estado_devuelto."""
    respuesta, codigo = servicios.estado_devuelto.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/editar_estado_devuelto.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/editar_estado_devuelto.html", **respuesta, **request.args)


@blueprint.route("/editar_estado_devuelto/<int:id>", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def estado_devuelto_id_editar(id):
    """Procesa editar_estado_devuelto."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nuevo_estado_devuelto, error = validadores.estado_devuelto.validar_nuevo(cuerpo)
    if nuevo_estado_devuelto is None:
        return redirect(url_for("admin.editar_estado_devuelto", id=id, **request.form, error=error))

    respuesta, codigo = servicios.estado_devuelto.actualizar_uno(id, nuevo_estado_devuelto)
    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.editar_estado_devuelto", id=id, **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("admin.editar_estado_devuelto", id=id, exito="Edicion Exitosa"))


@blueprint.route("/estado_devuelto/<int:id>/eliminar", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def estado_devuelto_id_eliminar(id):
    """Procesa eliminar estado_devuelto."""
    respuesta, codigo = servicios.estado_devuelto.eliminar_uno(id)

    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.estado_devuelto", error=respuesta.get("detalles")))

    return redirect(url_for("admin.estado_devuelto", exito=""))


@blueprint.route("/normativa", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def normativa():
    """Renderiza normativa."""
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

    filtros = {
        llave: valor
        for llave, valor in request.args.items()
        if llave not in ["pagina", "limite", "offset", "error"] and request.args.get(llave) != ""
    }
    filtros, error = validadores.normativa.validar_filtro(filtros)
    if filtros is None:
        return render_template("paginas/admin/normativa.html", error=error)

    respuesta, codigo = servicios.normativa.leer_paginado(pagina, limite, offset, filtros)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/normativa.html", error=respuesta.get("detalles"), **filtros)

    return render_template("paginas/admin/normativa.html", **respuesta, **filtros)


@blueprint.route("/normativa/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def normativa_id(id):
    """Renderiza normativa_id."""
    respuesta, codigo = servicios.normativa.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/normativa_id.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/normativa_id.html", **respuesta)


@blueprint.route("/nueva_normativa", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def nueva_normativa():
    """Renderiza nueva_normativa."""
    return render_template("paginas/admin/nueva_normativa.html", **request.args)


@blueprint.route("/nueva_normativa", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def nueva_normativa_post():
    """Procesa nueva_normativa."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nueva_normativa, error = validadores.normativa.validar_nuevo(cuerpo)
    if nueva_normativa is None:
        return redirect(url_for("admin.nueva_normativa", **request.form, error=error))

    respuesta, codigo = servicios.normativa.crear(nueva_normativa)
    if codigo != respuestas.CORRECTO:
        return redirect(url_for("admin.nueva_normativa", **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("admin.normativa_id", id=respuesta.get("datos").get("id")))


@blueprint.route("/editar_normativa/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def editar_normativa(id):
    """Renderiza editar_normativa."""
    respuesta, codigo = servicios.normativa.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/editar_normativa.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/editar_normativa.html", **respuesta, **request.args)


@blueprint.route("/editar_normativa/<int:id>", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def normativa_id_editar(id):
    """Procesa editar_normativa."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nueva_normativa, error = validadores.normativa.validar_nuevo(cuerpo)
    if nueva_normativa is None:
        return redirect(url_for("admin.editar_normativa", id=id, **request.form, error=error))

    respuesta, codigo = servicios.normativa.actualizar_uno(id, nueva_normativa)
    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.editar_normativa", id=id, **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("admin.editar_normativa", id=id, exito="Edicion Exitosa"))


@blueprint.route("/normativa/<int:id>/eliminar", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def normativa_id_eliminar(id):
    """Procesa eliminar normativa."""
    respuesta, codigo = servicios.normativa.eliminar_uno(id)

    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.normativa", error=respuesta.get("detalles")))

    return redirect(url_for("admin.normativa", exito=""))


@blueprint.route("/usuario", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def usuario():
    """Renderiza usuario."""
    pagina = request.args.get("pagina", 1)
    limite = request.args.get("limite", servicios.usuario.LIMITE_POR_DEFECTO)
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
    filtros, error = validadores.usuario.validar_filtro(filtros)
    if filtros is None:
        return render_template("paginas/admin/usuario.html", error=error)

    respuesta, codigo = servicios.usuario.leer_paginado(pagina, limite, offset, filtros)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/usuario.html", error=respuesta.get("detalles"), **filtros)

    return render_template("paginas/admin/usuario.html", **respuesta, **filtros)


@blueprint.route("/usuario/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def usuario_id(id):
    """Renderiza usuario_id."""
    respuesta, codigo = servicios.usuario.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/usuario_id.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/usuario_id.html", **respuesta)


@blueprint.route("/nuevo_usuario", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def nuevo_usuario():
    """Renderiza nuevo_usuario."""
    return render_template("paginas/admin/nuevo_usuario.html", **request.args)


@blueprint.route("/nuevo_usuario", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def nuevo_usuario_post():
    """Procesa nuevo_usuario."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nuevo_usuario, error = validadores.usuario.validar_nuevo(cuerpo)
    if nuevo_usuario is None:
        return redirect(url_for("admin.nuevo_usuario", error=error))

    respuesta, codigo = servicios.usuario.crear(nuevo_usuario)
    if codigo != respuestas.CORRECTO:
        return redirect(url_for("admin.nuevo_usuario", error=respuesta.get("detalles")))

    return redirect(url_for("admin.usuario_id", id=respuesta.get("datos").get("id")))


@blueprint.route("/editar_usuario/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def editar_usuario(id):
    """Renderiza editar_usuario."""
    respuesta, codigo = servicios.usuario.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/editar_usuario.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/editar_usuario.html", **respuesta, **request.args)


@blueprint.route("/editar_usuario/<int:id>", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def usuario_id_editar(id):
    """Procesa editar_usuario."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nuevo_usuario, error = validadores.usuario.validar_existente(cuerpo)
    if nuevo_usuario is None:
        return redirect(url_for("admin.editar_usuario", id=id, **request.form, error=error))

    respuesta, codigo = servicios.usuario.actualizar_uno(id, nuevo_usuario)
    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.editar_usuario", id=id, **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("admin.editar_usuario", id=id, exito="Edicion Exitosa"))


@blueprint.route("/usuario/<int:id>/eliminar", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def usuario_id_eliminar(id):
    """Procesa eliminar usuario."""
    respuesta, codigo = servicios.usuario.eliminar_uno(id)

    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.usuario", error=respuesta.get("detalles")))

    return redirect(url_for("admin.usuario", exito=""))


@blueprint.route("/reserva", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
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
        if llave not in ["pagina", "limite", "offset", "error"] and request.args.get(llave) != ""
    }
    filtros, error = validadores.reserva.validar_filtro(filtros)
    if filtros is None:
        return render_template("paginas/admin/reserva.html", error=error)

    respuesta, codigo = servicios.reserva.leer_paginado(pagina, limite, offset, filtros)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/reserva.html", error=respuesta.get("detalles"), **filtros)

    return render_template("paginas/admin/reserva.html", **respuesta, **filtros)


@blueprint.route("/reserva/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def reserva_id(id):
    """Renderiza reserva_id."""
    respuesta, codigo = servicios.reserva.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/reserva_id.html", error=respuesta.get("detalles"))

    qr_image = servicios.qr.generar_qr(url_for("publico.reserva_escaneo", id=id, _external=True))
    qr_src = f"data:[<mediatype>];base64,{qr_image}"

    return render_template("paginas/admin/reserva_id.html", **respuesta, qr_src=qr_src)


@blueprint.route("/nueva_reserva", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def nueva_reserva():
    """Renderiza nueva_reserva."""
    return render_template("paginas/admin/nueva_reserva.html", **request.args)


@blueprint.route("/nueva_reserva", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def nueva_reserva_post():
    """Procesa nueva_reserva."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nueva_reserva, error = validadores.reserva.validar_nuevo(cuerpo)
    if nueva_reserva is None:
        return redirect(url_for("admin.nueva_reserva", **request.form, error=error))

    respuesta, codigo = servicios.reserva.crear(nueva_reserva)
    if codigo != respuestas.CORRECTO:
        return redirect(url_for("admin.nueva_reserva", **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("admin.reserva_id", id=respuesta.get("datos").get("id")))


@blueprint.route("/editar_reserva/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def editar_reserva(id):
    """Renderiza editar_reserva."""
    respuesta, codigo = servicios.reserva.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/editar_reserva.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/editar_reserva.html", **respuesta, **request.args)


@blueprint.route("/editar_reserva/<int:id>", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def reserva_id_editar(id):
    """Procesa editar_reserva."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nueva_reserva, error = validadores.reserva.validar_nuevo(cuerpo)
    if nueva_reserva is None:
        return redirect(url_for("admin.editar_reserva", id=id, **request.form, error=error))

    respuesta, codigo = servicios.reserva.actualizar_uno(id, nueva_reserva)
    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.editar_reserva", id=id, **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("admin.editar_reserva", id=id, exito="Edicion Exitosa"))


@blueprint.route("/reserva/<int:id>/eliminar", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def reserva_id_eliminar(id):
    """Procesa eliminar reserva."""
    respuesta, codigo = servicios.reserva.eliminar_uno(id)

    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.reserva", error=respuesta.get("detalles")))

    return redirect(url_for("admin.reserva", exito=""))


@blueprint.route("/penalizacion", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def penalizacion():
    """Renderiza penalizacion."""
    pagina = request.args.get("pagina", 1)
    limite = request.args.get("limite", servicios.penalizacion.LIMITE_POR_DEFECTO)
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
    filtros, error = validadores.penalizacion.validar_filtro(filtros)
    if filtros is None:
        return render_template("paginas/admin/penalizacion.html", error=error)

    respuesta, codigo = servicios.penalizacion.leer_paginado(pagina, limite, offset, filtros)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/penalizacion.html", error=respuesta.get("detalles"), **filtros)

    return render_template("paginas/admin/penalizacion.html", **respuesta, **filtros)


@blueprint.route("/penalizacion/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def penalizacion_id(id):
    """Renderiza penalizacion_id."""
    respuesta, codigo = servicios.penalizacion.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/penalizacion_id.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/penalizacion_id.html", **respuesta)


@blueprint.route("/nueva_penalizacion", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def nueva_penalizacion():
    """Renderiza nueva_penalizacion."""
    return render_template("paginas/admin/nueva_penalizacion.html", **request.args)


@blueprint.route("/nueva_penalizacion", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def nueva_penalizacion_post():
    """Procesa nueva_penalizacion."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nueva_penalizacion, error = validadores.penalizacion.validar_nuevo(cuerpo)
    if nueva_penalizacion is None:
        return redirect(url_for("admin.nueva_penalizacion", **request.form, error=error))

    respuesta, codigo = servicios.penalizacion.crear(nueva_penalizacion)
    if codigo != respuestas.CORRECTO:
        return redirect(url_for("admin.nueva_penalizacion", **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("admin.penalizacion_id", id=respuesta.get("datos").get("id")))


@blueprint.route("/editar_penalizacion/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def editar_penalizacion(id):
    """Renderiza editar_penalizacion."""
    respuesta, codigo = servicios.penalizacion.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/editar_penalizacion.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/editar_penalizacion.html", **respuesta, **request.args)


@blueprint.route("/editar_penalizacion/<int:id>", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def penalizacion_id_editar(id):
    """Procesa editar_penalizacion."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nueva_penalizacion, error = validadores.penalizacion.validar_nuevo(cuerpo)
    if nueva_penalizacion is None:
        return redirect(url_for("admin.editar_penalizacion", id=id, **request.form, error=error))

    respuesta, codigo = servicios.penalizacion.actualizar_uno(id, nueva_penalizacion)
    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.editar_penalizacion", id=id, **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("admin.editar_penalizacion", id=id, exito="Edicion Exitosa"))


@blueprint.route("/penalizacion/<int:id>/eliminar", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def penalizacion_id_eliminar(id):
    """Procesa eliminar penalizacion."""
    respuesta, codigo = servicios.penalizacion.eliminar_uno(id)

    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.penalizacion", error=respuesta.get("detalles")))

    return redirect(url_for("admin.penalizacion", exito=""))


@blueprint.route("/faq", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def faq():
    """Renderiza faq."""
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

    filtros = {
        llave: valor
        for llave, valor in request.args.items()
        if llave not in ["pagina", "limite", "offset", "error"] and request.args.get(llave) != ""
    }
    filtros, error = validadores.faq.validar_filtro(filtros)
    if filtros is None:
        return render_template("paginas/admin/faq.html", error=error)

    respuesta, codigo = servicios.faq.leer_paginado(pagina, limite, offset, filtros)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/faq.html", error=respuesta.get("detalles"), **filtros)

    return render_template("paginas/admin/faq.html", **respuesta, **filtros)


@blueprint.route("/faq/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def faq_id(id):
    """Renderiza faq_id."""
    respuesta, codigo = servicios.faq.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/faq_id.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/faq_id.html", **respuesta)


@blueprint.route("/nueva_faq", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def nueva_faq():
    """Renderiza nueva_faq."""
    return render_template("paginas/admin/nueva_faq.html", **request.args)


@blueprint.route("/nueva_faq", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def nueva_faq_post():
    """Procesa nueva_faq."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nueva_faq, error = validadores.faq.validar_nueva(cuerpo)
    if nueva_faq is None:
        return redirect(url_for("admin.nueva_faq", **request.form, error=error))

    respuesta, codigo = servicios.faq.crear(nueva_faq)
    if codigo != respuestas.CORRECTO:
        return redirect(url_for("admin.nueva_faq", **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("admin.faq_id", id=respuesta.get("datos").get("id")))


@blueprint.route("/editar_faq/<int:id>", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def editar_faq(id):
    """Renderiza editar_faq."""
    respuesta, codigo = servicios.faq.leer_uno(id)
    if codigo != respuestas.CORRECTO:
        return render_template("paginas/admin/editar_faq.html", error=respuesta.get("detalles"))

    return render_template("paginas/admin/editar_faq.html", **respuesta, **request.args)


@blueprint.route("/editar_faq/<int:id>", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def faq_id_editar(id):
    """Procesa editar_faq."""
    cuerpo = {llave: valor for llave, valor in request.form.items()}
    nueva_faq, error = validadores.faq.validar_nueva(cuerpo)
    if nueva_faq is None:
        return redirect(url_for("admin.editar_faq", id=id, **request.form, error=error))

    respuesta, codigo = servicios.faq.actualizar_uno(id, nueva_faq)
    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.editar_faq", id=id, **request.form, error=respuesta.get("detalles")))

    return redirect(url_for("admin.editar_faq", id=id, exito="Edicion Exitosa"))


@blueprint.route("/faq/<int:id>/eliminar", methods=["POST"])
@autenticacion.requiere_rol(["admin"])
def faq_id_eliminar(id):
    """Procesa eliminar faq."""
    respuesta, codigo = servicios.faq.eliminar_uno(id)

    if codigo != respuestas.SIN_CONTENIDO:
        return redirect(url_for("admin.faq", error=respuesta.get("detalles")))

    return redirect(url_for("admin.faq", exito=""))


@blueprint.route("/reportes", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def reportes():
    """Renderiza la vista de reportes para administradores."""
    return "on development"


@blueprint.route("/reportes/morosidad", methods=["GET"])
@autenticacion.requiere_rol(["admin"])
def reporte_morosidad():
    """Renderiza morosidad."""
    return "on development"
