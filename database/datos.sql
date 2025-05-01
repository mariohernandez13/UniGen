-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS UniGen;

USE UniGen;

-- usuarios de prueba
INSERT INTO usuario (username, email, password, telefono, pais, edad, foto) VALUES
('admin', 'admin@unigen.com', 'admin', '600000001', 'España', 40, 'default-avatar.svg'),
('chusito', 'chusox@example.com', 'chuso', '612345678', 'México', 28, 'default-avatar.svg'),
('pasitos', 'pazix@example.com', 'pazos', '622334455', 'Argentina', 35, 'default-avatar.svg'),
('niklas', 'nico@gmail.com', 'ellolo', '611998877', 'Chile', 31, 'default-avatar.svg'),
('marito', 'mario@correo.com', 'marito', '655443322', 'Colombia', 22, 'default-avatar.svg'),
('super', 'gonyi@correo.com', 'super', '645675465', 'España', 22, 'default-avatar.svg');


-- Insertar actividades de prueba
INSERT INTO actividad (nombre,fecha, hora, lugar, tipo, descripcion, duracion)
VALUES
('Clase Magistral de Inteligencia Artificial', '2025-07-10', '10:00:00', 'Sala 102', 'charla', 'Explora los fundamentos y aplicaciones de la inteligencia artificial.', 150),
('Taller de Robótica', '2025-07-12', '14:00:00', 'Laboratorio 3', 'taller', 'Aprende a construir y programar robots con Arduino.', 120),
('Cine Científico', '2025-07-15', '18:00:00', 'Sala Audiovisual', 'ocio', 'Proyección de documental sobre ciencia y tecnología.', 90),
('Hackatón Universitaria', '2025-07-20', '08:00:00', 'Sala Multiusos', 'ocio', 'Desafío de programación intensivo de 12 horas.', 720),
('Sesión de Meditación Guiada', '2025-07-22', '16:30:00', 'Sala Zen', 'ayuda', 'Espacio de relajación y mindfulness para estudiantes.', 60),
('Torneo de Videojuegos', '2025-07-25', '13:00:00', 'Sala de Juegos', 'ocio', 'Competencia de FIFA, Smash Bros y más.', 180),
('Feria de Proyectos', '2025-07-28', '10:00:00', 'Pasillos de Ingeniería', 'taller', 'Estudiantes presentan sus trabajos finales.', 240),
('Charla sobre Energías Renovables', '2025-07-30', '11:00:00', 'Auditorio B', 'charla', 'Análisis del futuro de la energía sostenible.', 120),
('Taller de Diseño 3D', '2025-08-02', '15:00:00', 'Laboratorio CAD', 'taller', 'Aprende a modelar en 3D con Blender.', 150),
('Rally de Conocimientos', '2025-08-05', '09:00:00', 'Explanada Central', 'ocio', 'Actividad lúdica de preguntas y desafíos.', 180),
('Exposición de Arte Digital', '2025-08-07', '13:00:00', 'Galería Campus', 'ocio', 'Muestra de arte creado por estudiantes con herramientas digitales.', 240),
('Orientación Vocacional', '2025-10-12', '10:30:00', 'Sala de Orientación', 'ayuda', 'Ayuda a los estudiantes a elegir su camino profesional.', 120),
('Taller de Ciberseguridad', '2025-08-12', '12:30:00', 'Aula TIC', 'taller', 'Conceptos básicos para protegerse en internet.', 120),
('Taller de Resolución de Conflictos', '2025-10-05', '11:00:00', 'Sala de Mediación', 'ayuda', 'Aprende a resolver conflictos de manera efectiva.', 120),
('Charla de Emprendimiento', '2025-08-15', '10:30:00', 'Auditorio Principal', 'charla', 'Cómo iniciar tu propio negocio desde cero.', 90),
('Noche de Juegos de Mesa', '2025-08-18', '19:00:00', 'Cafetería Campus', 'deporte', 'Espacio para jugar UNO, Catán, ajedrez y más.', 150),
('Taller de Photoshop', '2025-08-20', '14:00:00', 'Sala Multimedia', 'taller', 'Aprende a editar imágenes con Photoshop.', 120),
('Torneo de Fútbol Rápido', '2025-08-22', '16:00:00', 'Cancha Techada', 'deporte', 'Equipos competirán en partidos de fútbol rápido.', 180),
('Comunicación Asertiva', '2025-10-03', '16:00:00', 'Sala de Conferencias', 'ayuda', 'Mejora tus habilidades de comunicación.', 90),
('Seminario de Ciencia de Datos', '2025-08-25', '09:30:00', 'Auditorio C', 'charla', 'Introducción a la ciencia de datos y machine learning.', 150),
('Taller de Realidad Aumentada', '2025-08-27', '13:00:00', 'Lab XR', 'taller', 'Crea tu primera app de realidad aumentada.', 120),
('Taller de Escritura Creativa', '2025-09-15', '13:00:00', 'Sala de Lectura', 'curso', 'Desarrolla tus habilidades narrativas y creativas.', 120),
('Gestión del Estrés', '2025-09-25', '14:00:00', 'Sala de Bienestar', 'ayuda', 'Aprende a manejar el estrés académico.', 120),
('Concurso de Memes Académicos', '2025-08-30', '17:00:00', 'Sala de Creatividad', 'curso', 'Los estudiantes presentarán sus mejores memes educativos.', 60),
('Taller de Programación en Python', '2025-09-02', '10:00:00', 'Aula 101', 'curso', 'Aprende a programar en Python desde cero.', 180),
('Caminata por la Naturaleza', '2025-09-05', '08:00:00', 'Entrada Principal', 'deporte', 'Disfruta de una caminata guiada por el campus.', 120),
('Taller de Fotografía Digital', '2025-09-07', '14:00:00', 'Sala de Arte', 'taller', 'Captura momentos únicos con tu cámara.', 150),
('Taller de Autoestima y Confianza', '2025-10-08', '14:00:00', 'Sala de Desarrollo Personal', 'ayuda', 'Fortalece tu autoestima y confianza personal.', 150),
('Charla sobre Blockchain', '2025-09-10', '11:00:00', 'Auditorio D', 'charla', 'Entiende el funcionamiento de la tecnología blockchain.', 120),
('Torneo de Ajedrez', '2025-09-12', '16:00:00', 'Sala de Juegos', 'deporte', 'Competencia de ajedrez entre estudiantes.', 180),
('Conferencia sobre Salud Mental', '2025-09-18', '10:30:00', 'Auditorio E', 'ayuda', 'Charlas sobre la importancia de la salud mental en estudiantes.', 90),
('Taller de Cocina Internacional', '2025-09-20', '18:00:00', 'Cocina del Campus', 'curso', 'Aprende a cocinar platos típicos de diferentes países.', 150),
('Mindfulness', '2025-09-22', '17:00:00', 'Sala de Meditación', 'ayuda', 'Técnicas de relajación y atención plena.', 90),
('Habilidades Sociales', '2025-09-28', '10:00:00', 'Sala de Conferencias', 'ayuda', 'Desarrolla tus habilidades interpersonales.', 150),
('Autocuidado', '2025-10-01', '13:00:00', 'Sala de Bienestar', 'ayuda', 'Aprende a cuidar de ti mismo y tu bienestar.', 120),
('Taller de Prevención del Acoso Escolar', '2025-10-10', '17:00:00', 'Auditorio F', 'ayuda', 'Prevención y manejo del acoso escolar.', 90),
('Club de Lectura', '2025-08-10', '17:00:00', 'Sala de Estudio', 'charla', 'Discusión de libros seleccionados por los estudiantes.', 90);

-- Actualizar las fotos de las actividades según el tipo
UPDATE actividad
SET foto = CASE
    WHEN tipo = 'charla' THEN 'charla.jpg'
    WHEN tipo = 'taller' THEN 'taller.jpg'
    WHEN tipo = 'deporte' THEN 'deporte.jpg'
    WHEN tipo = 'curso' THEN 'curso.jpg'
    WHEN tipo = 'ayuda' THEN 'ayuda.jpg'
    WHEN tipo = 'ocio' THEN 'ocio.jpg'
    ELSE 'default.png' -- Foto por defecto para tipos no válidos
END;

-- Insertar tipos de actividades
INSERT INTO tipo (nombre, imagen) VALUES
('charla', 'static/IMAGES/charla.jpg'),
('taller', 'static/IMAGES/taller.jpg'),
('deporte', 'static/IMAGES/deporte.jpg'),
('curso', 'static/IMAGES/curso.jpg'),
('ayuda', 'static/IMAGES/ayuda.jpg'),
('ocio', 'static/IMAGES/ocio.jpg');

-- Insertar relaciones de participación
INSERT INTO participacion ( idusuario, idactividad,puntos)
VALUES (1, 1, 10), (2, 1, 15), (3, 2, 20);

-- Insertar relaciones de creación (Usuarios que han creado actividades)
INSERT INTO creacion (idusuario, idactividad)
VALUES (1, 1), (2, 2), (3, 3);