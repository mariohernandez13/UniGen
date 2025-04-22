// Manejar envío del formulario de contacto
document.getElementById('contactForm').addEventListener('submit', function (e) {
    e.preventDefault();

    // Validar el formulario antes de continuar
    if (!this.checkValidity()) {
        // Mostrar errores de validación HTML5 (como "Campo obligatorio")
        this.reportValidity();
        return; // Detener el envío si no es válido
    }

    // Solo procesar si el formulario es válido
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    console.log("Formulario enviado:", data);

    // Mostrar toast de éxito
    const toast = new bootstrap.Toast(document.getElementById('successToast'));
    toast.show();

    // Resetear formulario y cerrar modal
    this.reset();
    bootstrap.Modal.getInstance(document.getElementById('contactModal')).hide();
});

// Validación en tiempo real 
document.querySelectorAll('#contactForm .form-control').forEach(input => {
    input.addEventListener('input', function () {
        const isValid = this.checkValidity();
        this.classList.toggle('is-invalid', !isValid);
        this.classList.toggle('is-valid', isValid);
    });
});
