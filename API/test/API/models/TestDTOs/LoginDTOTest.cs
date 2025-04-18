using System.ComponentModel.DataAnnotations;
using API.Models;
using Xunit;

namespace API.test.API.models.TestDTOs
{
    public class LoginDTOTest
    {
        [Fact]
        public void LoginDTO_Should_Have_Required_Username()
        {
            // Arrange
            var loginDTO = new LoginDTO { password = "password123" };

            // Act
            var validationContext = new ValidationContext(loginDTO);
            var validationResults = new List<ValidationResult>();
            var isValid = Validator.TryValidateObject(loginDTO, validationContext, validationResults, true);

            // Assert
            Assert.False(isValid);
            Assert.Contains(validationResults, v => v.MemberNames.Contains("username"));
        }

        [Fact]
        public void LoginDTO_Should_Have_Required_Password()
        {
            // Arrange
            var loginDTO = new LoginDTO { username = "user123" };

            // Act
            var validationContext = new ValidationContext(loginDTO);
            var validationResults = new List<ValidationResult>();
            var isValid = Validator.TryValidateObject(loginDTO, validationContext, validationResults, true);

            // Assert
            Assert.False(isValid);
            Assert.Contains(validationResults, v => v.MemberNames.Contains("password"));
        }

        [Fact]
        public void LoginDTO_Should_Be_Valid_When_All_Required_Fields_Are_Present()
        {
            // Arrange
            var loginDTO = new LoginDTO { username = "user123", password = "password123" };

            // Act
            var validationContext = new ValidationContext(loginDTO);
            var validationResults = new List<ValidationResult>();
            var isValid = Validator.TryValidateObject(loginDTO, validationContext, validationResults, true);

            // Assert
            Assert.True(isValid);
            Assert.Empty(validationResults);
        }
    }
}