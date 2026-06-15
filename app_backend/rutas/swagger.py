"""Implementa funcionalidad de swagger ui."""

from flask import send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

from config import DIRECTORIO_LOCAL

SWAGGER_YAML_URL = "/swagger.yaml"
blueprint = get_swaggerui_blueprint("/", SWAGGER_YAML_URL, config={"app_name": "TP Integrador API"})


@blueprint.route(SWAGGER_YAML_URL)
def swagger():
    """Sirve el archivo de especificación OpenAPI."""
    return send_from_directory(DIRECTORIO_LOCAL, "swagger.yaml")
