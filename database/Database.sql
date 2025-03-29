CREATE DATABASE UniGen;
USE UniGen;

CREATE TABLE usuario (
    idusuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    passwordHash VARCHAR(255)
);

CREATE TABLE actividad (
    idactividad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    fecha DATE,
    lugar VARCHAR(255),
    descripcion TEXT,
    duracion INT
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
