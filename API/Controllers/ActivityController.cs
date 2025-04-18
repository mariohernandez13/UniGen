using API.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;
using System.Linq;

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
    /// Obtener una actividad por ID.
    /// </summary>
    /// <param name="actividad"></param>
    /// <returns></returns>
    [HttpPost("create")]
    public async Task<IActionResult> CrearActividad([FromBody] Actividad actividad)
    {
        if (!ModelState.IsValid)
            return BadRequest(new { message = "Datos inválidos", errors = ModelState });

        _context.actividad.Add(actividad);
        await _context.SaveChangesAsync();
        return Ok(new { message = "Actividad creada exitosamente", actividad });
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
        actividadExistente.lugar = actividad.lugar;
        actividadExistente.duracion = actividad.duracion;

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
        return Ok(new { message = "Desinscripción exitosa" });
    }
}