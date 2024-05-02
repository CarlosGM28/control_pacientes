document.addEventListener("DOMContentLoaded", function() {
    const body = document.body;
    const images = [
        "url('../static/storage/login_1.jpg')",
        "url('../static/storage/login_2.jpg')",
        "url('../static/storage/login_3.jpg')"
    ];
    let currentIndex = 0;

    function changeBackground() {
        body.style.backgroundImage = images[currentIndex];
        body.style.transition = "background-image 1s ease-in-out"; // Agrega una transición suave
        currentIndex = (currentIndex + 1) % images.length;
    }

    // Cambia la imagen de fondo cada 5 segundos (5000 milisegundos)
    setInterval(changeBackground, 3000);
});

document.addEventListener("DOMContentLoaded", function() {
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const usernameIcon = document.getElementById('username-icon');
    const passwordIcon = document.getElementById('password-icon');

    // Función para activar la animación del icono
    function activateIcon(icon) {
        icon.classList.add('active');
    }

    // Función para desactivar la animación del icono
    function deactivateIcon(icon) {
        icon.classList.remove('active');
    }

    // Escuchar el evento de enfoque en los campos de entrada
    usernameInput.addEventListener('focus', () => activateIcon(usernameIcon));
    passwordInput.addEventListener('focus', () => activateIcon(passwordIcon));

    // Escuchar el evento de pérdida de enfoque en los campos de entrada
    usernameInput.addEventListener('blur', () => deactivateIcon(usernameIcon));
    passwordInput.addEventListener('blur', () => deactivateIcon(passwordIcon));
});

document.addEventListener("DOMContentLoaded", function() {
    const passwordInput = document.getElementById('password');
    const showPasswordCheckbox = document.getElementById('showPassword');

    showPasswordCheckbox.addEventListener('change', function() {
        if (this.checked) {
            passwordInput.setAttribute('type', 'text');
        } else {
            passwordInput.setAttribute('type', 'password');
        }
    });
});

