using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi.Models;

var builder = WebApplication.CreateBuilder(args);

// Configurar CORS para permitir solicitudes desde localhost y 127.0.0.1
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

// Configurar DbContext
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

builder.Services.AddDbContext<MiDbContext>(options =>
    options.UseMySQL(connectionString));

// Agregar servicios de Swagger
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "API UniGen", Version = "v1" });
});

builder.Services.AddControllers();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI(c => c.SwaggerEndpoint("/swagger/v1/swagger.json", "API UniGen v1"));
}

//  IMPORTANTE: CORS va antes de Authorization o cualquier otro middleware
app.UseCors("AllowFrontend");

app.UseAuthorization();

app.MapControllers();

app.Run();






