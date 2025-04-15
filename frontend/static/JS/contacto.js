// Script para el modal de contacto
const modal = document.getElementById("contactModal");
const openBtn = document.getElementById("openModal");
const closeBtn = document.querySelector(".close-btn");
const contactForm = document.getElementById("contactForm");

// Abrir modal
openBtn.addEventListener("click", () => {
    modal.style.display = "block";
    document.body.style.overflow = "hidden"; // Evitar scroll del fondo
});

// Cerrar modal
closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
    document.body.style.overflow = "auto";
});

// Cerrar al hacer clic fuera del modal
window.addEventListener("click", (e) => {
    if (e.target === modal) {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }
});

// Manejar envío del formulario
contactForm.addEventListener("submit", (e) => {
    e.preventDefault();
    
    // Aquí iría la lógica para enviar el formulario
    const formData = new FormData(contactForm);
    const data = Object.fromEntries(formData.entries());
    
    console.log("Formulario enviado:", data);
    
    // Mostrar mensaje de éxito (simulado)
    alert("¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.");
    
    // Resetear formulario y cerrar modal
    contactForm.reset();
    modal.style.display = "none";
    document.body.style.overflow = "auto";
});

// Cerrar con tecla ESC
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal.style.display === "block") {
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }
});