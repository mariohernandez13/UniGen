-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS UniGen;
USE UniGen;

-- Crear la tabla de usuario
CREATE TABLE IF NOT EXISTS usuario (
    idusuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

-- Crear la tabla de actividad
CREATE TABLE IF NOT EXISTS actividad (
    idactividad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    fecha DATE,
    lugar VARCHAR(255),
    descripcion TEXT,
    duracion INT
);

-- Crear la tabla de participacion
CREATE TABLE IF NOT EXISTS participacion (
    idusuario INT,
    idactividad INT,
    puntos INT DEFAULT 0,
    PRIMARY KEY (idusuario, idactividad),
    FOREIGN KEY (idusuario) REFERENCES usuario(idusuario) ON DELETE CASCADE,
    FOREIGN KEY (idactividad) REFERENCES actividad(idactividad) ON DELETE CASCADE
);

-- Crear la tabla de creacion
CREATE TABLE IF NOT EXISTS creacion (
    idusuario INT,
    idactividad INT,
    PRIMARY KEY (idusuario, idactividad),
    FOREIGN KEY (idusuario) REFERENCES usuario(idusuario) ON DELETE CASCADE,
    FOREIGN KEY (idactividad) REFERENCES actividad(idactividad) ON DELETE CASCADE
);

INSERT INTO usuario (username, nombre, apellido, email, password) VALUES
('Juanito', 'Juan', 'Pérez', 'juan.perez@email.com', '1234'),
('Maria','María', 'López', 'maria.lopez@email.com', '5678'),
('Carlos', 'Carlos', 'Gómez', 'carlos.gomez@email.com', 'admin');

-- Insertar actividades de prueba
INSERT INTO actividad (nombre, fecha, lugar, descripcion, duracion) VALUES
('Taller de Programación', '2025-04-10', 'Sala 101', 'Un taller para mejorar habilidades en Python.', 120),
('Conferencia de Tecnología', '2025-05-15', 'Auditorio Principal', 'Un evento sobre las últimas tendencias en tecnología.', 180),
('Torneo de Ajedrez', '2025-06-20', 'Sala de Juegos', 'Competencia amistosa de ajedrez.', 90);

-- Insertar relaciones de participación
INSERT INTO participacion (idusuario, idactividad, puntos) VALUES
(1, 1, 10),
(2, 1, 15),
(3, 2, 20);

-- Insertar relaciones de creación (Usuarios que han creado actividades)
INSERT INTO creacion (idusuario, idactividad) VALUES
(1, 1),
(2, 2),
(3, 3);
