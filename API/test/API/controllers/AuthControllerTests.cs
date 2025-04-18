using System.Linq.Expressions;
using API.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Moq;
using Xunit;

namespace API.test.API.controllers
{
    public class AuthControllerTests
    {
        private readonly Mock<MiDbContext> _mockContext;
        private readonly Mock<DbSet<Usuario>> _mockSet;
        private readonly AuthController _controller;

        public AuthControllerTests()
        {
            // Configurar el mock del DbSet
            _mockSet = new Mock<DbSet<Usuario>>();

            // Configurar el mock del DbContext
            _mockContext = new Mock<MiDbContext>();
            _mockContext.Setup(c => c.usuario).Returns(_mockSet.Object);

            // Crear el controlador con el DbContext simulado
            _controller = new AuthController(_mockContext.Object);
        }

        [Fact]
        public async Task GetUsers_ReturnsOkResult_WithListOfUsers()
        {
            // Arrange
            var users = new List<Usuario>
            {
                new() { idusuario = 1, username = "user1", email = "user1@example.com" },
                new() { idusuario = 2, username = "user2", email = "user2@example.com" }
            }.AsQueryable();

            _mockSet.As<IQueryable<Usuario>>().Setup(m => m.Provider).Returns(users.Provider);
            _mockSet.As<IQueryable<Usuario>>().Setup(m => m.Expression).Returns(users.Expression);
            _mockSet.As<IQueryable<Usuario>>().Setup(m => m.ElementType).Returns(users.ElementType);
            _mockSet.As<IQueryable<Usuario>>().Setup(m => m.GetEnumerator()).Returns(users.GetEnumerator());

            // Act
            var result = await _controller.GetUsers();

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            var returnValue = Assert.IsType<List<Usuario>>(okResult.Value);
            Assert.Equal(2, returnValue.Count);
        }

        [Fact]
        public async Task Registro_ReturnsConflict_WhenEmailExists()
        {
            // Arrange
            _mockSet.Setup(m => m.AnyAsync(It.IsAny<Expression<Func<Usuario, bool>>>(), default))
                    .ReturnsAsync(true);

            var userDto = new UsuarioDTO { email = "existing@example.com" };

            // Act
            var result = await _controller.Registro(userDto);

            // Assert
            var conflictResult = Assert.IsType<ConflictObjectResult>(result);
            Assert.Equal("El correo electrónico o el nombre de usuario ya están en uso.", ((dynamic?)conflictResult.Value)?.message);
        }

        [Fact]
        public async Task Login_ReturnsUnauthorized_WhenCredentialsAreInvalid()
        {
            // Arrange
            _mockSet.Setup(m => m.FirstOrDefaultAsync(It.IsAny<Expression<Func<Usuario, bool>>>(), default))
                    .ReturnsAsync((Usuario?)null);

            var loginDto = new LoginDTO { username = "user", password = "wrongpassword" };

            // Act
            var result = await _controller.Login(loginDto);

            // Assert
            var unauthorizedResult = Assert.IsType<UnauthorizedObjectResult>(result);
            Assert.Equal("Usuario o contraseña incorrectos", ((dynamic?)unauthorizedResult.Value)?.message);
        }

        [Fact]
        public async Task UpdateUser_ReturnsNotFound_WhenUserDoesNotExist()
        {
            // Arrange
            _mockSet.Setup(m => m.FindAsync(It.IsAny<object[]>())).ReturnsAsync((Usuario?)null);

            // Act
            var result = await _controller.UpdateUser(1, new Usuario());

            // Assert
            Assert.IsType<NotFoundResult>(result);
        }

        [Fact]
        public async Task DeleteUser_ReturnsOk_WhenUserIsDeleted()
        {
            // Arrange
            var user = new Usuario { idusuario = 1 };
            _mockSet.Setup(m => m.FindAsync(It.IsAny<object[]>())).ReturnsAsync(user);

            // Act
            var result = await _controller.DeleteUser(1);

            // Assert
            var okResult = Assert.IsType<OkObjectResult>(result);
            Assert.Equal("Usuario eliminado", ((dynamic?)okResult.Value)?.message);
        }
    }
}