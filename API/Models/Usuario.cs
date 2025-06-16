using System.ComponentModel.DataAnnotations;
using System.Diagnostics.CodeAnalysis;

namespace API.Models
{
    public class Usuario
    {
        [Key]
        public int idusuario { get; set; }

        public string? username { get; set; }

        public string? email { get; set; }

        public string? password { get; set; }

        public string? telefono { get; set; }

        public string? pais { get; set; }

        public int edad { get; set; }

        public string? foto { get; set; }  // Nombre de archivo o ruta

        public int puntos { get; set; }  // Puntos acumulados por el usuario
        public int papeletas { get; set; }  // Papeletas acumuladas por el usuario

        public DateTime? descuento_hasta { get; set; }
        public DateTime? bonus_creditos_hasta { get; set; }

        // Propiedad de navegación
        public ICollection<Participacion>? Participaciones { get; set; }

    }
}
