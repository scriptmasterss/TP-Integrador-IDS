ARG MYPORT

FROM python:3.13-slim

# Mantener la salida de Python sin buffer y evitar archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Habilitar compilación de bytecode para un inicio más rápido
ENV UV_COMPILE_BYTECODE=1
# Desactiva el pinning de Python en uv
ENV UV_PYTHON_CONTROL=0
# Indica a uv dónde colocar la caché
ENV UV_CACHE_DIR=/app/.uv_cache

# Copiar los binarios uv/uvx desde la imagen upstream para usar en la instalación de dependencias
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN groupadd --system tpIntegral && useradd --system -g tpIntegral tpIntegral

WORKDIR /app

COPY . .

# Instalar dependencias fijadas usando uv
RUN uv sync --frozen --no-install-project --no-dev

RUN chown -R tpIntegral:tpIntegral /app

EXPOSE ${MYPORT}

USER tpIntegral

CMD ["uv", "run", "python", "app.py"]
