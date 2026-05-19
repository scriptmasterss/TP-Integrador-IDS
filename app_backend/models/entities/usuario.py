from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(UserMixin):
    # pre: recibe un id, nombre de usuario, contraseña hasheada y nombre completo en formato texto
    # post: Inicializa las variables y retorna una instancia de la clase User
    def __init__(self, id_usuario, mail, constrasenia, nombre=""):
        self.id = id_usuario
        self.mail = mail       
        self.password = constrasenia
        self.full_name = nombre

    # pre: recibe el hash almacenado en la base de datos y la contraseña plana ingresada por el usuario
    # post: devuelve True si la contraseña plana coincide con el hash, False caso contrario
    @classmethod
    def check_password(cls, hashed_password, constrasenia_plana):
        coinciden_credenciales = check_password_hash(hashed_password, constrasenia_plana)
        return coinciden_credenciales