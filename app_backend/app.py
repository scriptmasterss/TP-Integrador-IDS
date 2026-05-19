import mysql.connector
from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user
from models.entities.usuario import User
from models.entities.modelo_usuario import ModelUser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_tp_2026'

gestor_login = LoginManager(app)

# pre: -
# post: devuelve un objeto de conexión activa a la base de datos mediante mysql.connector
def obtener_conexion_mysql():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="biblioteca"
    )
    return conexion

# pre: Recibe un JSON con las claves 'username' y 'password' a través del método POST.
# post: Inicia sesión validando credenciales, cierra la conexión y retorna JSON con el estado HTTP.
@app.route('/api/login', methods=['POST'])
def api_login():
    datos_peticion = request.json
    mensaje_respuesta = {}
    codigo_estado = 400
    conexion_mysql = None
    usuario_logueado = None
    
    usuario_intento = User(0, datos_peticion['mail'], datos_peticion['password'])
    
    try:
        conexion_mysql = obtener_conexion_mysql()
        usuario_logueado = ModelUser.login(conexion_mysql, usuario_intento)

        if usuario_logueado is not None:
            if User.check_password(usuario_logueado.password, usuario_intento.password):
                login_user(usuario_logueado)
                mensaje_respuesta = {"mensaje": "Inicio de sesión exitoso", "usuario": usuario_logueado.full_name}  # ← adentro del if
                codigo_estado = 200
            else:
                mensaje_respuesta = {"mensaje": "Contraseña inválida"}
                codigo_estado = 401
        else:
            mensaje_respuesta = {"mensaje": "Usuario no encontrado"}
            codigo_estado = 404
            
    finally:
        if conexion_mysql is not None and conexion_mysql.is_connected():
            conexion_mysql.close()

    return jsonify(mensaje_respuesta), codigo_estado

@gestor_login.user_loader
def cargar_usuario(id_usuario):
    conexion = obtener_conexion_mysql()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, mail, contrasenia_hash FROM usuario WHERE id = %s", (id_usuario,))
    fila = cursor.fetchone()
    return User(fila[0], fila[2], fila[3], fila[1]) if fila else None

if __name__ == '__main__':
    app.run(debug=True, port=5000)  