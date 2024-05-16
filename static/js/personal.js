document.addEventListener('DOMContentLoaded', function () {
    // Animación para mostrar elementos del menú
    const items = document.querySelectorAll('#navegador ul li');
    items.forEach((item, index) => {
        setTimeout(() => {
            item.classList.add('show');
        }, index * 100);
    });
});

$(document).ready(function() {
    $.ajax({
        url: '/registros_pacientes_medicos',
        type: "GET",
        success: function(response) {
            console.log(response);
            $('#data_table').DataTable({
                pageLength: 10,
                data: response["datos"],
                columns: [
                    { data: 'nombre' },
                    { data: 'dni' },
                    { data: 'email' },
                    { data: 'telefono' },
                    { data: 'especialidad' },
                    { data: 'rol' },
                    { data: 'hora_actual' },
                    { data: 'genero' },
                    {
                     data: null,
                        render: function(data, type, row) {
                            return '<div class="d-flex justify-content-center">' +
                            '<button class="btn btn-info ver-detalles" style="margin-right: 5px;"><i class="fas fa-eye"></i></button>' +
                            '<button class="btn btn-warning editar" style="margin-right: 5px;"><i class="fas fa-pencil-alt"></i></button>' +
                            '<button class="btn btn-danger eliminar" style="margin-right: 5px;"><i class="fas fa-trash-alt"></i></button>' +
                            '</div>';
                        }
                    }
                ],
                columnDefs: [
                    {
                        targets: -1,
                        orderable: false,
                        searchable: false
                    }
                ],
                scrollX: true,
                scrollY: 642,
                language: {
                    "lengthMenu": "Mostrar _MENU_ entradas por página", // Cambiar nombre de entradas por página
                    "search": "Buscar:", // Cambiar texto de búsqueda
                }
            });

            // Manejar clics en los botones
            $('#data_table tbody').on('click', '.ver-detalles', function() {
                var data = $('#data_table').DataTable().row($(this).parents('tr')).data();
                // Lógica para mostrar detalles
                console.log('Detalles del paciente:', data);
            });

            $('#data_table tbody').on('click', '.editar', function() {
                var data = $('#data_table').DataTable().row($(this).parents('tr')).data();
                // Lógica para editar
                console.log('Editar paciente:', data);
            });

            $('#data_table tbody').on('click', '.eliminar', function() {
                var data = $('#data_table').DataTable().row($(this).parents('tr')).data();
                // Lógica para eliminar
                console.log('Eliminar paciente:', data);
            });
        }
    });
});

// JavaScript para animar los campos de entrada
const animatedInputs = document.querySelectorAll('.animated-input');

animatedInputs.forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.querySelector('.animated-label').classList.add('active');
    });

    input.addEventListener('blur', function() {
        if (this.value === '') {
            this.parentElement.querySelector('.animated-label').classList.remove('active');
        }
    });
});

// JavaScript para cada campo de entrada, textarea, select y date
const inputsAndTextareasAndSelectAndDate = document.querySelectorAll('.input-container input, .input-container textarea, .input-container select, .input-container input[type="date"]');

inputsAndTextareasAndSelectAndDate.forEach(element => {
    const label = element.nextElementSibling;

    element.addEventListener('focus', () => {
        label.style.top = '-10px';
        label.style.fontSize = '12px';
        label.style.backgroundColor = 'white'; /* Fondo blanco */
        label.style.color = 'dodgerblue';
    });

    element.addEventListener('blur', () => {
        if (element.value === '' && element.tagName !== 'SELECT') {
            label.style.top = '10px';
            label.style.fontSize = '';
            label.style.backgroundColor = 'white'; /* Fondo blanco */
            label.style.color = '#aaa';
        } else if (element.tagName === 'SELECT') {
            // Si es un select, solo cambia la posición del label si no se ha seleccionado ningún valor
            if (element.value === '') {
                label.style.top = '10px';
                label.style.fontSize = '';
                label.style.backgroundColor = 'white'; /* Fondo blanco */
                label.style.color = '#aaa';
            }
        } else if (element.type === 'date') {
            // Si es un input de tipo date, verifica si la fecha está seleccionada
            if (element.value === '') {
                label.style.top = '10px';
                label.style.fontSize = '';
                label.style.backgroundColor = 'white'; /* Fondo blanco */
                label.style.color = '#aaa';
            }
        }
    });
});

// Función para cargar la API de Google Maps
(function() {
  var script = document.createElement("script");
  script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyDlWgApK6mth70OIyxMvQjpvRvA5dAaX5c"; // Reemplaza 'YOUR_API_KEY' con tu propia clave de API
  script.defer = true;
  script.onload = initMap; // Llamar a initMap una vez que la API de Google Maps se haya cargado
  document.head.appendChild(script);
})();

// Función para inicializar el mapa y agregar el evento clic para mostrar el modal
function initMap() {
  var mapDiv = document.getElementById("map");
  var map = new google.maps.Map(mapDiv, { 
    center: {lat: -8.3895368, lng: -74.5755113}, // Coordenadas de ejemplo
    zoom: 14 // Nivel de zoom de ejemplo
  });

  // Agregar evento clic al mapa
  map.addListener('click', function(event) {
      console.log("Clic en el mapa:", event.latLng); // Imprimir la ubicación en la consola
      showModal(event.latLng);
  });

}

// Función para mostrar el modal con la ubicación donde se hizo clic
function showModal(latLng) {
  var modal = document.getElementById("myModal");
  var span = document.getElementsByClassName("close")[0];
  modal.style.display = "block";

  // Cuando el usuario hace clic en (x), cierra el modal
  span.onclick = function() {
      modal.style.display = "none";
  }

  // Cuando el usuario hace clic fuera del modal, cierra el modal
  window.onclick = function(event) {
      if (event.target == modal) {
          modal.style.display = "none";
      }
  }

  // Rellenar los campos del formulario con la ubicación
  document.getElementById('latitud').value = latLng.lat();
  document.getElementById('logitud').value = latLng.lng();
}