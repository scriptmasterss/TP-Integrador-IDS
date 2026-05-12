from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config.from_object('app_backend.config')

    @app.route('/')
    def main():
        return {"mensaje": "Hola Mundo"}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0',
            port=5000)
