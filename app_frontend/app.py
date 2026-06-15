"""Punto de entrada de la aplicacion frontend."""

from flask import Flask

import config
import rutas

app = Flask(__name__, template_folder="plantiallas", static_folder="staticos", static_url_path="/staticos")

app.config["SECRET_KEY"] = config.SECRET_KEY
app.secret_key = config.SECRET_KEY

app.register_blueprint(rutas.publico.blueprint, url_prefix="/")
app.register_blueprint(rutas.alumno.blueprint, url_prefix="/alumno")
app.register_blueprint(rutas.profesor.blueprint, url_prefix="/profesor")
app.register_blueprint(rutas.bibliotecario.blueprint, url_prefix="/bibliotecario")
app.register_blueprint(rutas.admin.blueprint, url_prefix="/admin")

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
