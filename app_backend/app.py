"""Punto de entrada de la aplicación Flask del backend."""

from flask import Flask

import config
import rutas
from database import init_database

app = Flask(__name__)

init_database()

app.register_blueprint(rutas.articulos.blueprint, url_prefix="/api/articulos")
app.register_blueprint(rutas.autenticacion.blueprint, url_prefix="/api/autenticacion")
app.register_blueprint(rutas.estado_devuelto.blueprint, url_prefix="/api/estado_devuelto")
app.register_blueprint(rutas.faq.blueprint, url_prefix="/api/faq")
app.register_blueprint(rutas.normativa.blueprint, url_prefix="/api/normativa")
app.register_blueprint(rutas.penalizacion.blueprint, url_prefix="/api/penalizacion")
app.register_blueprint(rutas.qr.blueprint, url_prefix="/api/qr")
app.register_blueprint(rutas.reserva.blueprint, url_prefix="/api/reserva")
app.register_blueprint(rutas.salud.blueprint)
app.register_blueprint(rutas.swagger.blueprint)
app.register_blueprint(rutas.usuario.blueprint, url_prefix="/api/usuario")

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
