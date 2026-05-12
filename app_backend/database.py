import mysql.connector
import os

def obtener_conexion():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'db'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', 'root'),
            database=os.environ.get('DB_NAME'),
            port=os.environ.get('DB_PORT', 3306)
        )
        return connection
    
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None