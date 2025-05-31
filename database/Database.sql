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
    puntos INT DEFAULT 0,
    PRIMARY KEY (idusuario, idactividad),
    FOREIGN KEY (idusuario) REFERENCES usuario(idusuario),
    FOREIGN KEY (idactividad) REFERENCES actividad(idactividad)
);

CREATE TABLE creacion (
    idusuario INT,
    idactividad INT,
    PRIMARY KEY (idusuario, idactividad),
    FOREIGN KEY (idusuario) REFERENCES usuario(idusuario),
    FOREIGN KEY (idactividad) REFERENCES actividad(idactividad)
);
