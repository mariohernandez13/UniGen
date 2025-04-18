using Microsoft.AspNetCore.Cors.Infrastructure;
using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi.Models;
using Swashbuckle.AspNetCore.Swagger;
using Xunit;

namespace API.test.API.ProgramTest;
public class ProgramTest
{
    [Fact]
    public void TestCorsPolicyConfiguration()
    {
        // Arrange
        var builder = WebApplication.CreateBuilder();
        builder.Services.AddCors(options =>
        {
            options.AddPolicy("AllowFrontend", policy =>
            {
                policy
                    .WithOrigins("http://localhost:5000", "http://127.0.0.1:5000")
                    .AllowAnyHeader()
                    .AllowAnyMethod();
            });
        });

        var app = builder.Build();

        // Act
        var corsPolicy = app.Services.GetService<ICorsPolicyProvider>();

        // Assert
        Assert.NotNull(corsPolicy);
    }

    [Fact]
    public void TestDbContextConfiguration()
    {
        // Arrange
        var builder = WebApplication.CreateBuilder();
        var connectionString = "Server=localhost;Database=TestDb;User=root;Password=;";
        builder.Services.AddDbContext<MiDbContext>(options =>
            options.UseMySQL(connectionString));

        var app = builder.Build();

        // Act
        var dbContext = app.Services.GetService<MiDbContext>();

        // Assert
        Assert.NotNull(dbContext);
    }

}
