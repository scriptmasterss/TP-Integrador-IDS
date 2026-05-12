import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')
DB_NAME = os.environ.get('DB_NAME', 'sistema_prestamos')
DB_PORT = os.environ.get('DB_PORT', 3306)