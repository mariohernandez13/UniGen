using System.ComponentModel.DataAnnotations;
using API.Models;
using Xunit;

namespace API.test.API.models.TestDTOs
{
    public class UsuarioDTOTest
    {
        [Fact]
        public void UsuarioDTO_ValidData_ShouldPassValidation()
        {
            // Arrange
            var usuario = new UsuarioDTO
            {
                username = "testuser",
                password = "password123",
                email = "testuser@example.com",
                telefono = "123456789",
                pais = "USA",
                edad = 25
            };

            // Act
            var validationResults = ValidateModel(usuario);

            // Assert
            Assert.Empty(validationResults);
        }

        [Fact]
        public void UsuarioDTO_MissingRequiredFields_ShouldFailValidation()
        {
            // Arrange
            var usuario = new UsuarioDTO
            {
                telefono = "123456789",
                pais = "USA",
                edad = 25
            };

            // Act
            var validationResults = ValidateModel(usuario);

            // Assert
            Assert.NotEmpty(validationResults);
            Assert.Contains(validationResults, v => v.MemberNames.Contains("username"));
            Assert.Contains(validationResults, v => v.MemberNames.Contains("password"));
            Assert.Contains(validationResults, v => v.MemberNames.Contains("email"));
        }

        private IList<ValidationResult> ValidateModel(object model)
        {
            var validationResults = new List<ValidationResult>();
            var validationContext = new ValidationContext(model, null, null);
            Validator.TryValidateObject(model, validationContext, validationResults, true);
            return validationResults;
        }
    }
}