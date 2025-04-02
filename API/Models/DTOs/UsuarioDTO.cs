using System.ComponentModel.DataAnnotations;

namespace API.Models
{
    public class UsuarioDTO
    {
        [Required]
        public string username { get; set; }

        [Required]
        public string password { get; set; }
    }
}