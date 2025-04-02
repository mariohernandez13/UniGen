using System.ComponentModel.DataAnnotations;
using System.Diagnostics.CodeAnalysis;

namespace API.Models
{
    public class Usuario
    {
        [Key]
        public int idusuario { get; set; }
        public string username { get; set; }
        public string email { get; set; } 
        public string password { get; set; } 
    }
}
