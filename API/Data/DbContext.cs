using API.Models;
using Microsoft.EntityFrameworkCore;
public class MiDbContext : DbContext
{
    public MiDbContext(DbContextOptions<MiDbContext> options) : base(options) { }
    public DbSet<Usuario> Usuarios { get; set; }
}
