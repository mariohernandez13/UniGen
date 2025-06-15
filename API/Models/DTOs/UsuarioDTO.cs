using System.ComponentModel.DataAnnotations;

namespace API.Models
{
    public class UsuarioDTO
    {
        [Required]
        public string? username { get; set; }

        [Required]
        public string? password { get; set; }

        [Required]
        public string? email { get; set; }

        public string? telefono { get; set; }

        public string? pais { get; set; }

        public int edad { get; set; }
        public string? foto { get; set; }

        public int puntos { get; set; }
        public int papeletas { get; set; }
    }
}