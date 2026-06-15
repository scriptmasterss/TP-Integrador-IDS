SET
  NAMES utf8mb4;

SET
  time_zone = '-03:00';

SET
  lc_time_names = 'es_ES';

CREATE TABLE IF NOT EXISTS usuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  legajo INT UNIQUE DEFAULT NULL,
  nombre VARCHAR(50) NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL,
  rol enum('alumno', 'profesor', 'bibliotecario', 'admin') NOT NULL DEFAULT 'alumno',
  carrera enum(
    'Ingeniería Civil',
    'Ingeniería en Alimentos',
    'Ingeniería en Energía Eléctrica',
    'Ingeniería Electrónica',
    'Ingeniería en Agrimensura',
    'Ingeniería en Informática',
    'Ingeniería en Petróleo',
    'Ingeniería Industrial',
    'Ingeniería Mecánica',
    'Ingeniería Naval',
    'Ingeniería Química',
    'Lic. en Análisis de Sistemas',
    'Bioingeniería',
    'Desconocido'
  ) DEFAULT 'Desconocido',
  contrasenia_hash VARCHAR(255) NOT NULL,
  activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS articulos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL,
  tipo VARCHAR(50) NOT NULL DEFAULT 'varios',
  seccion VARCHAR(50) NOT NULL DEFAULT 'varios',
  stock INT DEFAULT 1,
  necesita_reparacion BOOLEAN DEFAULT FALSE,
  activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS reserva (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_articulo INT NOT NULL,
  estado_reserva enum(
    'pendiente',
    'aprobado',
    'rechazado',
    'entregado',
    'devuelto',
    'cancelado'
  ) NOT NULL DEFAULT 'pendiente',
  fecha_retiro DATETIME NOT NULL,
  fecha_regreso DATETIME NOT NULL,
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
  FOREIGN KEY (id_articulo) REFERENCES articulos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS estado_devuelto (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_reserva INT NOT NULL,
  dias_retraso INT NOT NULL DEFAULT 0,
  condiciones VARCHAR(255),
  FOREIGN KEY (id_reserva) REFERENCES reserva(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS penalizacion (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_usuario INT NOT NULL,
  id_reserva INT NOT NULL,
  motivo VARCHAR(255) NOT NULL,
  fecha_inicio DATETIME NOT NULL DEFAULT NOW(),
  fecha_fin DATETIME NOT NULL,
  activa BOOLEAN DEFAULT TRUE,
  severidad enum('baja', 'media', 'alta') NOT NULL DEFAULT 'media',
  FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE,
  FOREIGN KEY (id_reserva) REFERENCES reserva(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS faq (
  id INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(100),
  descripcion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS normativa (
  id INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(100),
  descripcion VARCHAR(255)
);
