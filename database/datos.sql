-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS UniGen;

USE UniGen;

-- usuarios de prueba
INSERT INTO usuario (username, email, password, telefono, pais, edad) VALUES
('admin', 'admin@unigen.com', 'admin', '600000001', 'España', 40),
('chusito', 'chusox@example.com', 'chuso', '612345678', 'México', 28),
('pasitos', 'pazix@example.com', 'pazos', '622334455', 'Argentina', 35),
('niklas', 'nico@gmail.com', 'ellolo', '611998877', 'Chile', 31),
('marito', 'mario@correo.com', 'marito', '655443322', 'Colombia', 22),
('super', 'gonyi@correo.com', 'super', '645675465', 'España', 22);

<<<<<<< HEAD
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

INSERT INTO usuario (idUsuario, username, email, password, telefono, pais, edad) 
VALUES 
(1, 'Juan Perez', 'juan.perez@example.com', 'password123', '123456789', 'Mexico', 30),
(2, 'Maria Lopez', 'maria.lopez@example.com', 'password123', '987654321', 'Argentina', 25),
(3, 'Carlos Gomez', 'carlos.gomez@example.com', 'password123', '456789123', 'Chile', 35),
(4, 'Ana Torres', 'ana.torres@example.com', 'password123', '789123456', 'Colombia', 28);
=======
>>>>>>> 98675a87e7bd6f48d8d431b09af81f4ffb616a54

-- Insertar actividades de prueba
INSERT INTO actividad (nombre,fecha, hora, lugar, tipo, descripcion, duracion)
VALUES
('Clase Magistral de Inteligencia Artificial', '2025-07-10', '10:00:00', 'Sala 102', 'charla', 'Explora los fundamentos y aplicaciones de la inteligencia artificial.', 150),
('Taller de Robótica', '2025-07-12', '14:00:00', 'Laboratorio 3', 'taller', 'Aprende a construir y programar robots con Arduino.', 120),
('Cine Científico', '2025-07-15', '18:00:00', 'Sala Audiovisual', 'recreativo', 'Proyección de documental sobre ciencia y tecnología.', 90),
('Hackatón Universitaria', '2025-07-20', '08:00:00', 'Sala Multiusos', 'competencia', 'Desafío de programación intensivo de 12 horas.', 720),
('Sesión de Meditación Guiada', '2025-07-22', '16:30:00', 'Sala Zen', 'bienestar', 'Espacio de relajación y mindfulness para estudiantes.', 60),
('Torneo de Videojuegos', '2025-07-25', '13:00:00', 'Sala de Juegos', 'juegos', 'Competencia de FIFA, Smash Bros y más.', 180),
('Feria de Proyectos', '2025-07-28', '10:00:00', 'Pasillos de Ingeniería', 'exposición', 'Estudiantes presentan sus trabajos finales.', 240),
('Charla sobre Energías Renovables', '2025-07-30', '11:00:00', 'Auditorio B', 'charla', 'Análisis del futuro de la energía sostenible.', 120),
('Taller de Diseño 3D', '2025-08-02', '15:00:00', 'Laboratorio CAD', 'taller', 'Aprende a modelar en 3D con Blender.', 150),
('Rally de Conocimientos', '2025-08-05', '09:00:00', 'Explanada Central', 'juegos', 'Actividad lúdica de preguntas y desafíos.', 180),
('Exposición de Arte Digital', '2025-08-07', '13:00:00', 'Galería Campus', 'exposición', 'Muestra de arte creado por estudiantes con herramientas digitales.', 240),
('Club de Lectura', '2025-08-10', '17:00:00', 'Sala de Estudio', 'charla', 'Discusión de libros seleccionados por los estudiantes.', 90),
('Taller de Ciberseguridad', '2025-08-12', '12:30:00', 'Aula TIC', 'taller', 'Conceptos básicos para protegerse en internet.', 120),
('Charla de Emprendimiento', '2025-08-15', '10:30:00', 'Auditorio Principal', 'charla', 'Cómo iniciar tu propio negocio desde cero.', 90),
('Noche de Juegos de Mesa', '2025-08-18', '19:00:00', 'Cafetería Campus', 'juegos', 'Espacio para jugar UNO, Catán, ajedrez y más.', 150),
('Taller de Photoshop', '2025-08-20', '14:00:00', 'Sala Multimedia', 'taller', 'Aprende a editar imágenes con Photoshop.', 120),
('Torneo de Fútbol Rápido', '2025-08-22', '16:00:00', 'Cancha Techada', 'competencia', 'Equipos competirán en partidos de fútbol rápido.', 180),
('Seminario de Ciencia de Datos', '2025-08-25', '09:30:00', 'Auditorio C', 'charla', 'Introducción a la ciencia de datos y machine learning.', 150),
('Taller de Realidad Aumentada', '2025-08-27', '13:00:00', 'Lab XR', 'taller', 'Crea tu primera app de realidad aumentada.', 120),
('Concurso de Memes Académicos', '2025-08-30', '17:00:00', 'Sala de Creatividad', 'recreativo', 'Los estudiantes presentarán sus mejores memes educativos.', 60);

-- Insertar relaciones de participación
INSERT INTO participacion ( idusuario, idactividad,puntos)
VALUES (1, 1, 10), (2, 1, 15), (3, 2, 20);

-- Insertar relaciones de creación (Usuarios que han creado actividades)
INSERT INTO creacion (idusuario, idactividad)
VALUES (1, 1), (2, 2), (3, 3);