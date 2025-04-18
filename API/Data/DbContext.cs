using API.Models;
using Microsoft.EntityFrameworkCore;
public class MiDbContext : DbContext
{
    public MiDbContext(DbContextOptions<MiDbContext> options) : base(options) { }
    public DbSet<Usuario> usuario { get; set; }
    public DbSet<Actividad> actividad { get; set; }
    public DbSet<Participacion> participacion { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Configurar clave primaria compuesta para Participacion
        modelBuilder.Entity<Participacion>()
            .HasKey(p => new { p.idusuario, p.idactividad });

        // Configurar relación entre Participacion y Usuario
        modelBuilder.Entity<Participacion>()
            .HasOne(p => p.Usuario)
            .WithMany(u => u.Participaciones)
            .HasForeignKey(p => p.idusuario);

        // Configurar relación entre Participacion y Actividad
        modelBuilder.Entity<Participacion>()
            .HasOne(p => p.Actividad)
            .WithMany(a => a.Participaciones)
            .HasForeignKey(p => p.idactividad);
    }

}

