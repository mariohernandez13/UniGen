using API.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;
using System.Linq;
using API.Models.DTOs;

/// <summary>
/// Controlador para gestionar actividades.
/// </summary>
[ApiController]
[Route("activity")]
public class ActivityController : ControllerBase
{
    private readonly MiDbContext _context;

    public ActivityController(MiDbContext context)
    {
        _context = context;
    }

    /// <summary>
    /// Obtener todas las actividades.
    /// </summary>
    /// <returns></returns>
    [HttpGet("all")]
    public async Task<IActionResult> GetActividades()
    {
        var actividades = await _context.actividad.ToListAsync();

        return Ok(actividades);
    }

    /// <summary>
    /// Obtener los IDs de las actividades en las que un usuario está inscrito.
    /// </summary>
    /// <param name="idUsuario">ID del usuario.</param>
    /// <returns>Lista de IDs de actividades.</returns>
    [HttpGet("user/{idUsuario}/subscriptions")]
    public async Task<IActionResult> ObtenerInscripciones(int idUsuario)
    {
        var inscripciones = await _context.participacion
            .Where(p => p.idusuario == idUsuario)
            .Select(p => p.idactividad) // Solo selecciona los IDs de las actividades
            .ToListAsync();

        return Ok(inscripciones);
    }

    /// <summary>
    /// Obtener participantes por id de actividad.
    /// </summary>
    /// <param name="idActividad">ID de la actividad.</param>
    /// <returns>Lista de participantes.</returns>
    [HttpGet("{idActividad}/participantes")]
    public async Task<IActionResult> ObtenerParticipantes(int idActividad)
    {
        var participantes = await _context.participacion
            .Where(p => p.idactividad == idActividad)
            .Select(p => new
            {
                p.idusuario,
                Nombre = _context.usuario
                    .Where(u => u.idusuario == p.idusuario)
                    .Select(u => u.username)
                    .FirstOrDefault()
            })
            .ToListAsync();
        
        return Ok(participantes);
    }

    /// <summary>
    /// Obtener una actividad por ID.
    /// </summary>
    /// <param name="actividad"></param>
    /// <returns></returns>
    [HttpPost("create")]
    public async Task<IActionResult> CrearActividad([FromBody] ActividadDTO actividadDTO)
    {
        if (!ModelState.IsValid)
            return BadRequest(new { message = "Datos inválidos", errors = ModelState });

        // Validar que el creador existe en la base de datos
        var creadorActividad = await _context.usuario
            .FirstOrDefaultAsync(u => u.idusuario == actividadDTO.CreadorId);

        if (creadorActividad == null)
            return NotFound(new { message = "Creador de la actividad no encontrado" });

        // Asignar una foto dependiendo del tipo de actividad
        string fotoAsignada = actividadDTO.Tipo.ToLower() switch
        {
            "ocio" => "ocio.jpg",
            "deporte" => "deporte.jpg",
            "curso" => "curso.jpg",
            "taller" => "taller.jpg",
            "charla" => "charla.jpg",
            "ayuda" => "ayuda.jpg",
            _ => "default.jpg"
        };

        // Convertir el DTO en una entidad Actividad
        var actividad = new Actividad
        {
            nombre = actividadDTO.Nombre,
            descripcion = actividadDTO.Descripcion,
            tipo = actividadDTO.Tipo,
            fecha = actividadDTO.Fecha,
            hora = actividadDTO.Hora,
            lugar = actividadDTO.Lugar,
            duracion = actividadDTO.Duracion,
            foto = fotoAsignada,
            creador = actividadDTO.CreadorId,  // Asignar el ID del creador
            Puntos = actividadDTO.Puntos // Asegúrate de que este campo exista en tu modelo
        };


        _context.actividad.Add(actividad);
        await _context.SaveChangesAsync();
        return Ok(new { message = "Actividad creada exitosamente", actividad });
    }

    /// <summary>
    /// Obtener detalles de actividades por IDs.
    /// </summary>
    /// <param name="actividadIds"></param>
    /// <returns></returns>
    [HttpPost("details")]
    public async Task<IActionResult> ObtenerDetallesActividades([FromBody] List<int> actividadIds)
    {
        var actividades = await _context.actividad
            .Where(a => actividadIds.Contains(a.idactividad))
            .ToListAsync();

        return Ok(actividades);
    }

    /// <summary>
    /// Inscribirse a una actividad.
    /// </summary>
    /// <param name="id"></param>
    /// <param name="idUsuario"></param>
    /// <returns></returns>
    [HttpPost("{id}/subscribe")]
    public async Task<IActionResult> Inscribirse(int id, [FromBody] int idUsuario)
    {
        var actividad = await _context.actividad.FindAsync(id);
        if (actividad == null)
            return NotFound(new { message = "Actividad no encontrada" });

        var usuario = await _context.usuario.FindAsync(idUsuario);
        if (usuario == null)
            return NotFound(new { message = "Usuario no encontrado" });

        // Verificar si ya está inscrito
        var participacionExistente = await _context.participacion
            .FirstOrDefaultAsync(p => p.idusuario == idUsuario && p.idactividad == id);
        if (participacionExistente != null)
            return Conflict(new { message = "El usuario ya está inscrito en esta actividad" });

        var participacion = new Participacion
        {
            idusuario = idUsuario,
            idactividad = id
        };

        _context.participacion.Add(participacion);
        await _context.SaveChangesAsync();
        return Ok(new { message = "Inscripción exitosa" });
    }


    /// <summary>
    /// Actualizar una actividad.
    /// </summary>
    /// <param name="id"></param>
    /// <param name="actividad"></param>
    /// <returns></returns>
    [HttpPut("update/{id}")]
    public async Task<IActionResult> EditarActividad(int id, [FromBody] Actividad actividad)
    {
        var actividadExistente = await _context.actividad.FindAsync(id);
        if (actividadExistente == null)
            return NotFound(new { message = "Actividad no encontrada" });

        actividadExistente.nombre = actividad.nombre;
        actividadExistente.descripcion = actividad.descripcion;
        actividadExistente.fecha = actividad.fecha;
        actividadExistente.hora = actividad.hora;
        actividadExistente.lugar = actividad.lugar;
        actividadExistente.duracion = actividad.duracion;
        actividadExistente.tipo = actividad.tipo;

        await _context.SaveChangesAsync();
        return Ok(new { message = "Actividad actualizada exitosamente", actividadExistente });
    }

    /// <summary>
    /// Eliminar una actividad.
    /// </summary>
    /// <param name="id"></param>
    /// <returns></returns>
    [HttpDelete("delete/{id}")]
    public async Task<IActionResult> BorrarActividad(int id)
    {
        var actividad = await _context.actividad.FindAsync(id);
        if (actividad == null)
            return NotFound(new { message = "Actividad no encontrada" });

        _context.actividad.Remove(actividad);
        await _context.SaveChangesAsync();
        return Ok(new { message = "Actividad eliminada exitosamente" });
    }

    /// <summary>
    /// Borrarse de una actividad.
    /// </summary>
    /// <param name="id">ID de la actividad.</param>
    /// <param name="idUsuario">ID del usuario que desea desinscribirse.</param>
    /// <returns>Mensaje de éxito o error.</returns>
    [HttpDelete("{id}/unsubscribe")]
    public async Task<IActionResult> Desinscribirse(int id, [FromBody] int idUsuario)
    {
        var participacion = await _context.participacion
            .FirstOrDefaultAsync(p => p.idactividad == id && p.idusuario == idUsuario);

        if (participacion == null)
            return NotFound(new { message = "No estás inscrito en esta actividad" });

        _context.participacion.Remove(participacion);
        await _context.SaveChangesAsync();
        return Ok(new { message = "Te has borrado de la actividad con éxito" });
    }

}