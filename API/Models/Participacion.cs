using System.ComponentModel.DataAnnotations;

namespace API.Models
{
    public class Participacion

    {
        public int idusuario { get; set; }
        public int idactividad { get; set; }
        
        // Propiedades de navegación
        public Usuario Usuario { get; set; }
        public Actividad Actividad { get; set; }
    }
}