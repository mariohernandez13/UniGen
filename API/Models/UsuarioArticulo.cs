using System;
using System.ComponentModel.DataAnnotations;

public class UsuarioArticulo
{
    [Key]
    public int id { get; set; }
    public int idusuario { get; set; }
    public string? articulo { get; set; }
    public DateTime fecha_compra { get; set; } = DateTime.Now;
}