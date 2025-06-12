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

        modelBuilder.Entity<Participacion>()
            .HasKey(p => new { p.idusuario, p.idactividad });

        modelBuilder.Entity<Participacion>()
            .HasOne(p => p.Usuario)
            .WithMany(u => u.Participaciones)
            .HasForeignKey(p => p.idusuario);

        modelBuilder.Entity<Participacion>()
            .HasOne(p => p.Actividad)
            .WithMany(a => a.Participaciones)
            .HasForeignKey(p => p.idactividad);

        modelBuilder.Entity<Participacion>()
            .Property(p => p.creditos_validados)
            .HasColumnType("tinyint(1)") // MySQL/MariaDB: bool <-> tinyint(1)
            .HasDefaultValue(false);
    }

}

