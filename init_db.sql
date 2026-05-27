CREATE TABLE IF NOT EXISTS usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    mail VARCHAR(50) UNIQUE NOT NULL,
    score INT DEFAULT 0
    estado_usuario VARCHAR(20) NOT NULL DEFAULT 'activo',
);

CREATE TABLE IF NOT EXISTS articulos (
    id_articulo INT AUTO_INCREMENT PRIMARY KEY,
    nombre_art VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    seccion VARCHAR(50) NOT NULL,
    prestacion_maxima INT NOT NULL,
    stock INT DEFAULT 1,
    necesita_reparacion BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_reservado INT NOT NULL,
    estado_reserva VARCHAR(20) NOT NULL DEFAULT 'pendiente',
    fecha_retiro DATETIME NOT NULL,
    fecha_regreso DATETIME NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id),
    FOREIGN KEY (id_reservado) REFERENCES articulos(id_articulo)
);

CREATE TABLE IF NOT EXISTS estado_devuelto (
    id_devuelto INT NOT NULL,
    dias_retraso INT DEFAULT 0,
    condiciones VARCHAR(50),
    FOREIGN KEY (id_devuelto) REFERENCES reserva(id_reserva)
);


ALTER TABLE usuario 
ADD rol VARCHAR(20) DEFAULT 'alumno';

ALTER TABLE usuario 
ADD carrera VARCHAR(50);

CREATE TABLE IF NOT EXISTS penalizacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    motivo VARCHAR(255),
    fecha_inicio DATETIME,
    fecha_fin DATETIME,
    activa BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);

CREATE TABLE IF NOT EXISTS qr (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT,
    fecha_generado DATETIME NOT NULL,
    codigo VARCHAR(255) UNIQUE,
    escaneado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

CREATE TABLE IF NOT EXISTS normativa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100),
    descripcion TEXT,
    fecha DATETIME
);
