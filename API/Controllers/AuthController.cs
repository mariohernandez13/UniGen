using API.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;
using System.Linq;
using System.Text.Json;

/// <summary>
/// Controlador para autenticación de usuarios.
/// </summary>
[ApiController]
[Route("auth")]
public class AuthController : ControllerBase
{
    private readonly MiDbContext _context;

    public AuthController(MiDbContext context)
    {
        _context = context;
    }

    /// <summary>
    /// Obtiene todos los usuarios.
    /// </summary>
    /// <returns>OK y lista de usuarios</returns>
    [HttpGet("users")]
    public async Task<IActionResult> GetUsers()
    {
        var usuarios = await _context.usuario.ToListAsync();
        return Ok(usuarios);
    }

    /// <summary>
    /// Registro de un nuevo usuario.
    /// </summary>
    /// <param name="userDto"></param>
    /// <returns></returns>
    [HttpPost("registro")]
    public async Task<IActionResult> Registro([FromBody] UsuarioDTO userDto)
    {

        // Verificar si ya existe un usuario con ese email o username
        var emailExiste = await _context.usuario.AnyAsync(u => u.email == userDto.email);
        // var userExiste = await _context.usuario.AnyAsync(u => u.username == userDto.username);

        if (emailExiste)
        {
            return Conflict(new { message = "El correo electrónico o el nombre de usuario ya están en uso." });
        }


        var usuario = new Usuario
        {
            username = userDto.username,
            email = userDto.email,
            password = userDto.password,
            telefono = userDto.telefono,
            pais = userDto.pais,
            edad = userDto.edad,
            foto = "default-avatar.svg",
            puntos = 0 // Inicializar puntos a 0
        };

        _context.usuario.Add(usuario);
        await _context.SaveChangesAsync();
        return Ok(new { message = "Usuario registrado exitosamente" });
    }

    /// <summary>
    /// Inicio de sesión de usuario.
    /// </summary>
    /// <param name="loginDto"></param>
    /// <returns>OK si es correcto y toda la info del usuario</returns>
    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginDTO loginDto)
    {
        var usuario = await _context.usuario
            .FirstOrDefaultAsync(u => u.username == loginDto.username && u.password == loginDto.password);

        if (usuario == null)
            return Unauthorized(new { message = "Usuario o contraseña incorrectos" });

        return Ok(new
        {
            message = "Inicio de sesión exitoso",
            usuario = new
            {
                usuario.idusuario,
                usuario.username,
                usuario.email,
                usuario.telefono,
                usuario.pais,
                usuario.edad,
                foto = usuario.foto ?? "default-avatar.svg",
                puntos = usuario.puntos 
            }
        });
    }


    /// <summary>
    /// Actualiza un usuario existente.
    /// </summary>
    /// <param name="id"></param>
    /// <param name="usuario"></param>
    /// <returns></returns>
    [HttpPut("update/{id}")]
    public async Task<IActionResult> UpdateUser(int id, [FromBody] UsuarioDTO usuario)
    {
        var existingUser = await _context.usuario.FindAsync(id);
        if (existingUser == null) return NotFound();

        existingUser.username = usuario.username;
        existingUser.email = usuario.email;
        existingUser.password = usuario.password;
        existingUser.telefono = usuario.telefono;
        existingUser.pais = usuario.pais;
        existingUser.edad = usuario.edad;
        existingUser.foto = usuario.foto ?? existingUser.foto;
        existingUser.puntos = usuario.puntos;


        await _context.SaveChangesAsync();
        return Ok(existingUser);
    }

    /// <summary>
    /// Elimina un usuario existente.
    /// </summary>
    /// <param name="id"></param>
    /// <returns></returns>
    [HttpDelete("delete/{id}")]
    public async Task<IActionResult> DeleteUser(int id)
    {
        var usuario = await _context.usuario.FindAsync(id);
        if (usuario == null) return NotFound();

        _context.usuario.Remove(usuario);
        await _context.SaveChangesAsync();
        return Ok(new { message = "Usuario eliminado" });
    }

    [HttpPut("usuario/{idusuario}/editar_perfil")]
    public async Task<IActionResult> EditarPerfil(int idusuario, [FromBody] JsonElement body)
    {
        var usuario = await _context.usuario.FindAsync(idusuario);
        if (usuario == null) return NotFound();

        usuario.username = body.GetProperty("username").GetString();
        usuario.email = body.GetProperty("email").GetString();
        usuario.telefono = body.GetProperty("telefono").GetString();
        if (body.TryGetProperty("foto", out var fotoProp))
            usuario.foto = fotoProp.GetString();

        await _context.SaveChangesAsync();
        return Ok();
    }

    [HttpPost("sumar_creditos")]
    public async Task<IActionResult> SumarCreditos([FromBody] JsonElement body)
    {
        int idusuario = body.GetProperty("idusuario").GetInt32();
        int idactividad = body.GetProperty("idactividad").GetInt32();
        int puntos = body.GetProperty("puntos").GetInt32();

        var usuario = await _context.usuario.FindAsync(idusuario);
        if (usuario == null) return NotFound();

        usuario.puntos = usuario.puntos + puntos;

        // Marca la participación como validada
        var participacion = await _context.participacion
            .FirstOrDefaultAsync(p => p.idusuario == idusuario && p.idactividad == idactividad);
        if (participacion != null)
        {
            participacion.creditos_validados = true;
            _context.Entry(participacion).Property(x => x.creditos_validados).IsModified = true;
        }

        await _context.SaveChangesAsync();

        return Ok(new { puntos = usuario.puntos });
    }
}
