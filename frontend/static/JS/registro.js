
const botonEnvio = document.getElementById("botonEnvio");
botonEnvio.addEventListener("click", validacionDatos);



function validacionDatos(event) {

    let nombre = document.forms[0][0];
    let apellidos = document.forms[0][1];
    let contrasenia = document.forms[0][2];
    let verContrasenia = document.forms[0][3];
    let correo = document.forms[0][4];
    let telefono = document.forms[0][5];
    let pais = document.forms[0][6];
    let edad = document.forms[0][7];
    let valido = true;
    let regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    let movilRegex = /^\+?[1-9]\d{1,14}$/;
    let edadRegex = /^[0-9]+$/;

    Evaluar(nombre); 

    if (valido) { // Si el nombre es valido pasa a evaluar los apellidos
        Evaluar(apellidos);
    }

    if (valido) {
        Evaluar(contrasenia);
    }

    if (valido) {
        VerificarContra(contrasenia, verContrasenia);
    }

    if (valido) { // Si el apellido es valido pasa a evaluar el correo
        EvaluarCorreo(correo);
    }

    if (valido) { // Si el correo es valido pasa a evaluar el movil
        EvaluarMovil(telefono);
    }

    if (valido) { // Si el movil es valido pasa a evaluar el pais
        Evaluar(pais);
    }

    if (valido) {
        EvaluarEdad(edad);
    }

    // if(!valido) { 
    //     event.preventDefault();
    // }
    

    function Evaluar(campo) { // Funcion basica para evaluar los elementos

        if (campo.value === "") {
            campo.classList.add("is-invalid");
            valido = false;
        }
        else {
            campo.classList.remove("is-invalid");
        }
    }
    
    function EvaluarCorreo(correo) { // Funcion para evaluar el correo
    
        if (!regex.test(correo.value)) {
            correo.classList.add("is-invalid");
            valido = false;
        }
        else {
            correo.classList.remove("is-invalid");
        }
    }

    function EvaluarMovil(movil) { // Funcion para evaluar el movil

        if (!movilRegex.test(movil.value)) {
            movil.classList.add("is-invalid");
            valido = false;
        }
        else {
            movil.classList.remove("is-invalid");
        }
    }

    function EvaluarEdad(edad) {
        if (edad.value == "" && !edadRegex.test(edad.value)) {
            edad.classList.add("is-invalid");
            valido = false;
        }
        else {
            edad.classList.remove("is-invalid");
        }
    }

    function VerificarContra(contra, verContra) {
        if (verContra.value === "" || contra.value != verContra.value) {
            verContra.classList.add("is-invalid");
            valido = false;
        }
        else {
            verContra.classList.remove("is-invalid");
        }
    }

}


