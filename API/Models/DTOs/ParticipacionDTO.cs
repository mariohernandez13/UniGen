using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace API.Models
{
    public class ParticipacionDTO
    {
        public int idusuario { get; set; }
        public int idactividad { get; set; }
        public int puntos { get; set; }
        public bool creditos_validados { get; set; } // <-- bool simple

        // Propiedades de navegación
        public Usuario Usuario { get; set; }
        public Actividad Actividad { get; set; }
    }
}