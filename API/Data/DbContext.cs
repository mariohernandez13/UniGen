using API.Models;
using Microsoft.EntityFrameworkCore;
public class MiDbContext : DbContext
{
    public MiDbContext(DbContextOptions<MiDbContext> options) : base(options) { }
    public DbSet<Usuario> usuario { get; set; }
    public DbSet<Actividad> actividad { get; set; }
    public DbSet<Participacion> participacion { get; set; }

}

