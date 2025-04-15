using System.ComponentModel.DataAnnotations;

namespace API.Models
{
    public class Participacion
    {
        [Key]
        public int idusuario { get; set; }
        public int idactividad { get; set; }
    }
}