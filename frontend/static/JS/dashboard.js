document.addEventListener('DOMContentLoaded', function(){


    let actividadSeleccionada = null;
    let botonSeleccionado = null;

    let botones = document.querySelectorAll(".mas_informacion");
    let i;
    let contador = 0;


    function Girar(event) {
        event.preventDefault();
        let carta = event.target.closest(".card");
        let titulo = carta.querySelector(".title-bg");
        let descripcion = carta.querySelector(".descripcion");
        let mapa = carta.querySelector(".mapa");
        let imagen = carta.querySelector(".card-img");
        let hora_lugar = carta.querySelectorAll(".mb-1");
        let organizador = carta.querySelector(".mb-3");
        let apuntarse = carta.querySelector(".apuntarse-btn");
        let girada = carta.classList.contains("carta_girada");
        if (!girada) {
            carta.style.transform = "rotateY(180deg)";
            carta.style.transformStyle = "preserve-3d";
            titulo.style.display = "none";
            descripcion.style.display = "block";
            descripcion.style.transform = "rotateY(180deg)";
            mapa.style.display = "block";
            mapa.style.transform = "rotateY(180deg)";
            imagen.style.display = "none";
            hora_lugar[0].style.display = "none";
            hora_lugar[1].style.display = "none";
            organizador.style.display = "none";
            apuntarse.style.display = "none";
            event.target.style.transform = "rotateY(180deg)";
            event.target.textContent = "Volver";
            carta.classList.add("carta_girada");
        }
        else {
            carta.style.transform = "rotateY(0deg)";
            carta.style.transformStyle = "preserve-3d";
            titulo.style.display = "block";
            descripcion.style.display = "none";
            descripcion.style.transform = "rotateY(0deg)";
            mapa.style.display = "none";
            mapa.style.transform = "rotateY(0deg)";
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
});