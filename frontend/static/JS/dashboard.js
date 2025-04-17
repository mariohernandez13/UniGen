let actividadSeleccionada = null;
let botonSeleccionado = null;

let botones = document.querySelectorAll("#mas_informacion");
let i;
let contador = 0;


function Girar(event) {
    let carta = event.target.closest(".card");
    let titulo = carta.querySelector(".title-bg");
    let imagen = carta.querySelector(".card-img");
    let hora_lugar = carta.querySelectorAll(".mb-1");
    let organizador = carta.querySelector(".mb-3");
    let apuntarse = carta.querySelector(".apuntarse-btn");
    let girada = carta.classList.contains("carta_girada");
    if (!girada) {
        carta.style.transform = "rotateY(180deg)";
        carta.style.transformStyle = "preserve-3d";
        titulo.style.display = "none";
        imagen.style.display = "none";
        hora_lugar[0].style.display = "none";
        hora_lugar[1].style.display = "none";
        organizador.style.display = "none";
        apuntarse.style.display = "none";
        event.target.style.transform = "rotateY(180deg)";
        event.target.textContent = "Volver";
        carta.classList.add("carta_girada");
    }
    else{
        carta.style.transform = "rotateY(0deg)";
        carta.style.transformStyle = "preserve-3d";
        titulo.style.display = "block";
        imagen.style.display = "block";
        hora_lugar[0].style.display = "block";
        hora_lugar[1].style.display = "block";
        organizador.style.display = "block";
        apuntarse.style.display = "block";
        event.target.style.transform = "rotateY(0deg)";
        event.target.textContent = "Más información";
        carta.classList.remove("carta_girada");
    }
}

for (i = 0; i < botones.length; i++) {
    botones[i].addEventListener("click", Girar);
}

// let cocina = document.getElementById("Cocina");
// let imagen_cocina = document.getElementById("imagen_cocina");
// let titulo_cocina = document.getElementById("titulo_cocina");
// let hora_cocina = document.getElementById("Hora");
// let lugar_cocina = document.getElementById("Lugar");
// let organizador_cocina = document.getElementById("Organizador");
// let fondo_cocina = document.getElementById("fondo_cocina");
// let apuntarse = document.getElementById("Apuntarse");
// let mas_informacion = document.getElementById("mas_informacion");

// function Girar() {
//     cocina.style.transform = "rotateY(180deg)";
//     cocina.style.transformStyle = "preserve-3d";
//     imagen_cocina.style.visibility = "hidden";
//     const descripcion = document.getElementById("descripcion_cocina");
//     descripcion.style.display = "none";
//     descripcion.style.transform = "rotateY(180deg)";
//     titulo_cocina.style.display = "none";
//     hora_cocina.style.display = "none";
//     lugar_cocina.style.display = "none";
//     organizador_cocina.style.display = "none";
//     fondo_cocina.style.display = "none";
//     mas_informacion.style.display = "none";
//     mas_informacion.textContent = "Volver";
//     mas_informacion.style.transform = "rotateY(180deg)";
//     apuntarse.style.display = "none";
// }



// Aplica solo a los botones de apuntarse (no al de más información)
document.querySelectorAll('.apuntarse-btn').forEach(boton => {
    boton.addEventListener('click', function (e) {
        e.preventDefault();

        const card = this.closest('.card');
        const nombreActividad = card.querySelector('.card-title').textContent;

        actividadSeleccionada = nombreActividad;
        botonSeleccionado = this;

        document.getElementById('nombreActividadModal').textContent = nombreActividad;

        const modal = new bootstrap.Modal(document.getElementById('confirmarModal'));
        modal.show();
    });
});

// Al confirmar el modal
document.getElementById('confirmarBtn').addEventListener('click', function () {
    if (botonSeleccionado) {
        botonSeleccionado.textContent = "Ya estás apuntado";
        botonSeleccionado.classList.add("bloqueado");



        // Ocultar el botón de "Más información"
        const botonMasInfo = botonSeleccionado.parentElement.querySelector('.btn-info');
        if (botonMasInfo) {
            botonMasInfo.style.display = 'none';
        }

    }

    const modal = bootstrap.Modal.getInstance(document.getElementById('confirmarModal'));
    modal.hide();
});