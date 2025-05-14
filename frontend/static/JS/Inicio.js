let botones = document.querySelectorAll(".mas_informacion");
let i;
let contador = 0;


function Girar(event) {
    event.preventDefault();
    let carta = event.target.closest(".card");
    let titulo = carta.querySelector(".title-bg");
    let descripcion = carta.querySelector(".descripcion");
    let imagen = carta.querySelector(".card-img");
    let hora_lugar = carta.querySelectorAll(".mb-1");
    let organizador = carta.querySelector(".mb-3");
    let desapuntarse = carta.querySelector(".btn-danger");
    let girada = carta.classList.contains("carta_girada");
    if (!girada) {
        carta.style.transform = "rotateY(180deg)";
        carta.style.transformStyle = "preserve-3d";
        titulo.style.display = "none";
        descripcion.style.display = "block";
        descripcion.style.transform = "rotateY(180deg)";
        imagen.style.display = "none";
        hora_lugar[0].style.display = "none";
        hora_lugar[1].style.display = "none";
        hora_lugar[2].style.display = "none";
        organizador.style.display = "none";
        desapuntarse.style.display = "none";
        event.target.style.transform = "rotateY(180deg)";
        event.target.textContent = "Volver";
        event.target.style.marginTop = "165px";
        carta.classList.add("carta_girada");
    }
    else {
        carta.style.transform = "rotateY(0deg)";
        carta.style.transformStyle = "preserve-3d";
        titulo.style.display = "block";
        descripcion.style.display = "none";
        descripcion.style.transform = "rotateY(0deg)";
        imagen.style.display = "block";
        hora_lugar[0].style.display = "block";
        hora_lugar[1].style.display = "block";
        hora_lugar[2].style.display = "block";
        organizador.style.display = "block";
        desapuntarse.style.display = "block";
        event.target.style.transform = "rotateY(0deg)";
        event.target.textContent = "Ver Detalles";
        event.target.style.marginTop = "0px";
        carta.classList.remove("carta_girada");
    }
}

for (i = 0; i < botones.length; i++) {
    botones[i].addEventListener("click", Girar);
}