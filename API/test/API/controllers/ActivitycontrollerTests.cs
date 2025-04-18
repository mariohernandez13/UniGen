using API.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Moq;
using Xunit;

namespace API.Test.Controllers
{
    public class ActivityControllerTests
    {
        private readonly Mock<MiDbContext> _mockContext;
        private readonly ActivityController _controller;

        public ActivityControllerTests()
        {
            _mockContext = new Mock<MiDbContext>();
            _controller = new ActivityController(_mockContext.Object);
        }

        [Fact]
        public async Task GetActividades_ReturnsOkResult_WithListOfActividades()
        {
            // Arrange
            var actividades = new List<Actividad>
            {
                new Actividad { idactividad = 1, nombre = "Actividad 1" },
                new Actividad { idactividad = 2, nombre = "Actividad 2" }
            };
            var mockSet = new Mock<DbSet<Actividad>>();
            mockSet.As<IQueryable<Actividad>>().Setup(m => m.Provider).Returns(actividades.AsQueryable().Provider);
            mockSet.As<IQueryable<Actividad>>().Setup(m => m.Expression).Returns(actividades.AsQueryable().Expression);
            mockSet.As<IQueryable<Actividad>>().Setup(m => m.ElementType).Returns(actividades.AsQueryable().ElementType);
            mockSet.As<IQueryable<Actividad>>().Setup(m => m.GetEnumerator()).Returns(actividades.AsQueryable().GetEnumerator());
            _mockContext.Setup(c => c.actividad).Returns(mockSet.Object);

            // Act
            var result = await _controller.GetActividades();

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var returnValue = Assert.IsType<List<Actividad>>(okResult.Value);
            Assert.Equal(2, returnValue.Count);
        }

        [Fact]
        public async Task ObtenerInscripciones_ReturnsOkResult_WithListOfActivityIds()
        {
            // Arrange
            int userId = 1;
            var participaciones = new List<Participacion>
            {
                new Participacion { idusuario = userId, idactividad = 1 },
                new Participacion { idusuario = userId, idactividad = 2 }
            };
            var mockSet = new Mock<DbSet<Participacion>>();
            mockSet.As<IQueryable<Participacion>>().Setup(m => m.Provider).Returns(participaciones.AsQueryable().Provider);
            mockSet.As<IQueryable<Participacion>>().Setup(m => m.Expression).Returns(participaciones.AsQueryable().Expression);
            mockSet.As<IQueryable<Participacion>>().Setup(m => m.ElementType).Returns(participaciones.AsQueryable().ElementType);
            mockSet.As<IQueryable<Participacion>>().Setup(m => m.GetEnumerator()).Returns(participaciones.AsQueryable().GetEnumerator());
            _mockContext.Setup(c => c.participacion).Returns(mockSet.Object);

            // Act
            var result = await _controller.ObtenerInscripciones(userId);

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var returnValue = Assert.IsType<List<int>>(okResult.Value);
            Assert.Equal(2, returnValue.Count);
        }

        [Fact]
        public async Task CrearActividad_ReturnsOkResult_WhenModelIsValid()
        {
            // Arrange
            var actividad = new Actividad { idactividad = 1, nombre = "Nueva Actividad" };
            var mockSet = new Mock<DbSet<Actividad>>();
            _mockContext.Setup(c => c.actividad).Returns(mockSet.Object);

            // Act
            var result = await _controller.CrearActividad(actividad);

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var returnValue = Assert.IsType<dynamic>(okResult.Value);
            Assert.Equal("Actividad creada exitosamente", returnValue.message);
        }

        [Fact]
        public async Task BorrarActividad_ReturnsOkResult_WhenActividadExists()
        {
            // Arrange
            int actividadId = 1;
            var actividad = new Actividad { idactividad = actividadId };
            var mockSet = new Mock<DbSet<Actividad>>();
            mockSet.Setup(m => m.FindAsync(actividadId)).ReturnsAsync(actividad);
            _mockContext.Setup(c => c.actividad).Returns(mockSet.Object);

            // Act
            var result = await _controller.BorrarActividad(actividadId);

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var returnValue = Assert.IsType<dynamic>(okResult.Value);
            Assert.Equal("Actividad eliminada exitosamente", returnValue.message);
        }

        [Fact]
        public async Task EditarActividad_ReturnsNotFound_WhenActividadDoesNotExist()
        {
            // Arrange
            int actividadId = 1;
            var actividad = new Actividad { idactividad = actividadId, nombre = "Updated" };
            var mockSet = new Mock<DbSet<Actividad>>();
            mockSet.Setup(m => m.FindAsync(actividadId)).ReturnsAsync((Actividad)null);
            _mockContext.Setup(c => c.actividad).Returns(mockSet.Object);

            // Act
            var result = await _controller.EditarActividad(actividadId, actividad);

            // Assert
            var notFoundResult = Assert.IsType<NotFoundObjectResult>(result);
            var returnValue = Assert.IsType<dynamic>(notFoundResult.Value);
            Assert.Equal("Actividad no encontrada", returnValue.message);
        }
    }
}