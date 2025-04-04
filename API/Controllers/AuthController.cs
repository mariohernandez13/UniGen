﻿using API.Models;
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
            username = userDto.username,
            password = userDto.password
        };

        _context.usuario.Add(usuario);
        await _context.SaveChangesAsync();
        return Ok(new { message = "Usuario registrado exitosamente" });
    }

    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] UsuarioDTO userDto)
    {
        var usuario = await _context.usuario
            .FirstOrDefaultAsync(u => u.username == userDto.username && u.password == userDto.password);

        if (usuario == null)
            return Unauthorized(new { message = "Usuario o contraseña incorrectos" });

        // Retornar un mensaje de éxito con los datos del usuario
        return Ok(new
        {
            message = "Inicio de sesión exitoso",
            usuario = new
            {
                usuario.idusuario,
                usuario.username
            }
        });
    }


    [HttpGet("users")]
    public async Task<IActionResult> GetUsers()
    {
        var usuarios = await _context.usuario.ToListAsync();
        return Ok(usuarios);
    }

    [HttpPut("update/{id}")]
    public async Task<IActionResult> UpdateUser(int id, [FromBody] Usuario usuario)
    {
        var existingUser = await _context.usuario.FindAsync(id);
        if (existingUser == null) return NotFound();

        existingUser.username = usuario.username;
        existingUser.email = usuario.email;
        existingUser.password = usuario.password;

        await _context.SaveChangesAsync();
        return Ok(existingUser);
    }

    [HttpDelete("delete/{id}")]
    public async Task<IActionResult> DeleteUser(int id)
    {
        var usuario = await _context.usuario.FindAsync(id);
        if (usuario == null) return NotFound();

        _context.usuario.Remove(usuario);
        await _context.SaveChangesAsync();
        return Ok(new { message = "Usuario eliminado" });
    }
}
