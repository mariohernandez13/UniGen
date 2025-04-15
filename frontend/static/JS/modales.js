// // Script para el modal de contacto
// const modal = document.getElementById("contactModal");
// const modalBackdrop = document.createElement("div");
// modalBackdrop.className = "modal-backdrop";
// document.body.appendChild(modalBackdrop);

// const openBtns = document.querySelectorAll("#openModal, #link5");
// const closeBtn = document.querySelector(".close-btn");
// const contactForm = document.getElementById("contactForm");

// function openModal() {
//     document.body.classList.add("modal-open");
//     modalBackdrop.style.display = "block";
//     modal.style.display = "block";
    
//     // Pequeño retraso para que la animación funcione correctamente
//     setTimeout(() => {
//         modalBackdrop.style.opacity = "1";
//     }, 10);
// }

// function closeModal() {
//     document.body.classList.remove("modal-open");
//     modal.style.display = "none";
//     modalBackdrop.style.display = "none";
// }

// // Event listeners para abrir el modal
// openBtns.forEach(btn => {
//     btn.addEventListener("click", openModal);
// });

// // Event listeners para cerrar el modal
// closeBtn.addEventListener("click", closeModal);

// // Cerrar al hacer clic fuera del modal
// modalBackdrop.addEventListener("click", closeModal);

// // Manejar envío del formulario
// contactForm.addEventListener("submit", (e) => {
//     e.preventDefault();
    
//     // Aquí iría la lógica para enviar el formulario
//     const formData = new FormData(contactForm);
//     const data = Object.fromEntries(formData.entries());
    
//     console.log("Formulario enviado:", data);
    
//     // Mostrar mensaje de éxito (simulado)
//     alert("¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.");
    
//     // Resetear formulario y cerrar modal
//     contactForm.reset();
//     closeModal();
// });

// // Cerrar con tecla ESC
// document.addEventListener("keydown", (e) => {
//     if (e.key === "Escape" && modal.style.display === "block") {
//         closeModal();
//     }
// });



// Manejar envío del formulario de contacto
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Aquí iría la lógica para enviar el formulario
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());
    
    console.log("Formulario enviado:", data);
    
    // Mostrar mensaje de éxito (simulado)
    alert("¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.");
    
    // Resetear formulario y cerrar modal
    this.reset();
    bootstrap.Modal.getInstance(document.getElementById('contactModal')).hide();
});

// Los modales ahora se manejan automáticamente por Bootstrap
// No necesitamos el código personalizado anterior