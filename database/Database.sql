DROP DATABASE IF EXISTS UniGen;

CREATE DATABASE UniGen;
USE UniGen;

CREATE TABLE usuario (
    idusuario INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    telefono VARCHAR(20),
    pais VARCHAR(50),
    edad INT,
    foto VARCHAR(255),
    puntos INT DEFAULT 0
);
-- TODO cambiar edad por fecha de nacimiento

CREATE TABLE actividad (
    idactividad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    fecha DATE,
    hora TIME,
    lugar VARCHAR(255),
    tipo VARCHAR(100),
    descripcion TEXT,
    duracion INT,
    foto VARCHAR(255),
    creador INT,
    puntos INT DEFAULT 0,
    FOREIGN KEY (creador) REFERENCES usuario(idusuario)
);

CREATE TABLE tipo (
    idtipo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    imagen VARCHAR(255) NOT NULL
);

CREATE TABLE participacion (
    idusuario INT,
    idactividad INT,
    creditos_validados TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (idusuario, idactividad),
    FOREIGN KEY (idusuario) REFERENCES usuario(idusuario),
    FOREIGN KEY (idactividad) REFERENCES actividad(idactividad) ON DELETE CASCADE
);

CREATE TABLE usuario_articulo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idusuario INT,
    articulo VARCHAR(100),
    fecha_compra DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idusuario) REFERENCES usuario(idusuario)
);