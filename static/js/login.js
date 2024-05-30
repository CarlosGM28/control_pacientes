$(document).ready(function() {
    $('#login-form').submit(function(event) {
        event.preventDefault();  // Evitar que el formulario se envíe de forma predeterminada

        // Mostrar el spinner y desactivar el botón de envío
        $('#loading-spinner').show();

        // Realizar una solicitud AJAX para enviar los datos del formulario
        $.ajax({
            url: '/login',
            type: 'POST',
            data: $(this).serialize(),  // Serializar los datos del formulario
            success: function(response) {
                // Ocultar el spinner y habilitar el botón de envío
                $('#loading-spinner').hide();
                $('#submit-button').prop('disabled', false).show();

                // Verificar si hay un mensaje de alerta en la respuesta
                if (response.mensaje_alerta) {
                    // Mostrar el mensaje de alerta en el contenedor
                    $('#alert-container').html('<label class="label-show-password"><span style="color: red;">' + response.mensaje_alerta + '</span></label>');
                } else if (response.redirect) {
                    // Redirigir al usuario a la página principal si no hay mensaje de alerta
                    window.location.href = response.redirect;
                }
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);

                // Ocultar el spinner y habilitar el botón de envío
                $('#loading-spinner').hide();
                $('#submit-button').prop('disabled', false).show();
            }
        });
    });
});


  // Obtener el diálogo y los botones para abrir y cerrar el popup
  const popup = document.getElementById('popup');
  const openButton = document.getElementById('openPopup');
  const closeButton = document.getElementById('closePopup');

  // Mostrar el popup al hacer clic en el botón de abrir
  openButton.addEventListener('click', function() {
    popup.showModal();
  });

  // Cerrar el popup al hacer clic en el botón de cerrar
  closeButton.addEventListener('click', function() {
    popup.close();
  });

  document.addEventListener("DOMContentLoaded", function () {
    var interval = setInterval(function () {
      var currentSlide = document.querySelector('input[name="slide"]:checked');
      var slides = document.querySelectorAll('input[name="slide"]');
      var nextSlide = currentSlide.nextElementSibling || slides[0];
      nextSlide.checked = true;
    }, 5000); // Cambia de slide cada 5 segundos (5000 milisegundos)
  });