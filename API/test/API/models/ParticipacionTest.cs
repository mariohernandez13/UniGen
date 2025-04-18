using Xunit;
using API.Models;

namespace API.test.Models
{
    public class ParticipacionTest
    {
        [Fact]
        public void Participacion_Should_SetAndGet_IdUsuario()
        {
            // Arrange
            var participacion = new Participacion();
            var expectedIdUsuario = 1;

            // Act
            participacion.idusuario = expectedIdUsuario;

            // Assert
            Assert.Equal(expectedIdUsuario, participacion.idusuario);
        }

        [Fact]
        public void Participacion_Should_SetAndGet_IdActividad()
        {
            // Arrange
            var participacion = new Participacion();
            var expectedIdActividad = 2;

            // Act
            participacion.idactividad = expectedIdActividad;

            // Assert
            Assert.Equal(expectedIdActividad, participacion.idactividad);
        }

        [Fact]
        public void Participacion_Should_SetAndGet_Usuario()
        {
            // Arrange
            var participacion = new Participacion();
            var expectedUsuario = new Usuario { idusuario = 1, username = "testuser" };

            // Act
            participacion.Usuario = expectedUsuario;

            // Assert
            Assert.Equal(expectedUsuario, participacion.Usuario);
        }

        [Fact]
        public void Participacion_Should_SetAndGet_Actividad()
        {
            // Arrange
            var participacion = new Participacion();
            var expectedActividad = new Actividad {  idactividad = 1, nombre = "test" };

            // Act
            participacion.Actividad = expectedActividad;

            // Assert
            Assert.Equal(expectedActividad, participacion.Actividad);
        }
    }
}