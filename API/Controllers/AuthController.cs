using API.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;
using System.Linq;

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

    [HttpPost("register")]
    public async Task<IActionResult> Register([FromBody] UsuarioDTO userDto)
    {
        var usuario = new Usuario
        {
            Username = userDto.Username,
            Password = userDto.Password
        };

        _context.Usuarios.Add(usuario);
        await _context.SaveChangesAsync();
        return Ok(new { message = "Usuario registrado exitosamente" });
    }

    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] UsuarioDTO userDto)
    {
        var usuario = await _context.Usuarios
            .FirstOrDefaultAsync(u => u.Username == userDto.Username && u.Password == userDto.Password);

        if (usuario == null)
            return Unauthorized(new { message = "Usuario o contraseña incorrectos" });

        // Retornar un mensaje de éxito con los datos del usuario
        return Ok(new
        {
            message = "Inicio de sesión exitoso",
            usuario = new
            {
                usuario.Id,
                usuario.Username
            }
        });
    }


    [HttpGet("users")]
    public async Task<IActionResult> GetUsers()
    {
        var usuarios = await _context.Usuarios.ToListAsync();
        return Ok(usuarios);
    }

    [HttpPut("update/{id}")]
    public async Task<IActionResult> UpdateUser(int id, [FromBody] Usuario usuario)
    {
        var existingUser = await _context.Usuarios.FindAsync(id);
        if (existingUser == null) return NotFound();

        existingUser.Username = usuario.Username;
        existingUser.Mail = usuario.Mail;
        existingUser.Password = usuario.Password;

        await _context.SaveChangesAsync();
        return Ok(existingUser);
    }

    [HttpDelete("delete/{id}")]
    public async Task<IActionResult> DeleteUser(int id)
    {
        var usuario = await _context.Usuarios.FindAsync(id);
        if (usuario == null) return NotFound();

        _context.Usuarios.Remove(usuario);
        await _context.SaveChangesAsync();
        return Ok(new { message = "Usuario eliminado" });
    }
}
