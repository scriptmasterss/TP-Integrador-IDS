import mysql.connector
from models.entities.usuario import User

class ModelUser:
    # pre: recibe un objeto de conexión de mysql.connector y una instancia de User con el username a buscar.
    # Post: devuelve una instancia de User con los datos obtenidos o None si no se encuentra en MySQL.
    @classmethod
    def login(cls, conexion_bd, usuario_intento):
        cursor_bd = None
        usuario_encontrado = None
        resultado_fila = None
        
        try:
            cursor_bd = conexion_bd.cursor()
            consulta_sql = "SELECT id, nombre, mail, contrasenia_hash FROM usuario WHERE mail = %s"
            cursor_bd.execute(consulta_sql, (usuario_intento.mail,))
            resultado_fila = cursor_bd.fetchone()

            if resultado_fila is not None:
                if resultado_fila is not None:
                    usuario_encontrado = User(
                        resultado_fila[0],  
                        resultado_fila[2],  
                        resultado_fila[3],  
                        resultado_fila[1]   
                    )
                
        except mysql.connector.Error as excepcion_bd:
            print(f"Error de base de datos: {excepcion_bd}")
            # mas adelante habría/tendría que mejorar esta parte
        finally:
            if cursor_bd is not None:
                cursor_bd.close()

        return usuario_encontrado