namespace API.Models.DTOs
{
    public class ActividadDTO
    {
        public int IdActividad { get; set; }
        public string? Nombre { get; set; }
        public string? Descripcion { get; set; }
        public string? Tipo { get; set; }
        public DateTime Fecha { get; set; }
        public TimeSpan Hora { get; set; }
        public string? Lugar { get; set; }
        public int Duracion { get; set; }
        public int CreadorId { get; set; }
        public int puntos { get; set; } // <--- ASEGÚRATE DE QUE EXISTE
        
    }
}