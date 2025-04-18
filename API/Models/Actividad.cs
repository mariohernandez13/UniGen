using System.ComponentModel.DataAnnotations;

namespace API.Models
{
    public class Actividad
    {
        [Key]
        public int idactividad { get; set; }
        public string nombre { get; set; }
        public string descripcion { get; set; }
        public string tipo { get; set; }
        public DateTime fecha { get; set; }
        public TimeSpan hora { get; set; }
        public string lugar { get; set; }
        public int duracion { get; set; }

        // Propiedad de navegación
        public ICollection<Participacion> Participaciones { get; set; }
    }
}