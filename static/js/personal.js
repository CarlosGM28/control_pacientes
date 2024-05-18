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
                    { data: 'estado' },
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

            // Manejar clics en los botones de editar
            $('#data_table tbody').on('click', '.editar', function() {
                var data = $('#data_table').DataTable().row($(this).parents('tr')).data();
                // Actualizar los campos del formulario en el modal con los datos del paciente
                $('#nombreEditar').val(data.nombre);
                $('#dniEditar').val(data.dni);
                $('#emailEditar').val(data.email);
                $('#telefonoEditar').val(data.telefono);
                $('#generoEditar').val(data.genero);
                $('#especialidadEditar').val(data.especialidad);
                $('#rolEditar').val(data.rol);
                $('#estadoEditar').val(data.estado);
                // Mostrar el modal para editar los datos
                $('#modal_personal_editar').modal('show');
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

  // Cargar datos de marcadores usando AJAX
  $.ajax({
    url: '/registros_pacientes',
    type: "GET",
    dataType: 'json', // Asegurarse de que jQuery interprete la respuesta como JSON
    success: function(data) {
      console.log('Datos recibidos:', data); // Verifica la estructura de los datos
      if (Array.isArray(data.datos)) {
        data.datos.forEach(function(location) {
          addMarker(location, map);
        });
      } else {
        console.error('La respuesta no contiene datos válidos:', data);
      }
    },
    error: function(error) {
      console.error('Error al cargar los datos:', error);
    }
  });

  // Agregar evento clic al mapa
  map.addListener('click', function(event) {
    console.log("Clic en el mapa:", event.latLng);
    showModal(event.latLng);
  });
}

// Función para agregar un marcador al mapa
function addMarker(location, map) {
    // Verificar si el estado es "Pendiente"
    if (location.estado !== "Pendiente") {
      return; // Si el estado no es "Pendiente", no agregar el marcador
    }
  
    var marker = new google.maps.Marker({
      position: {lat: parseFloat(location.lat), lng: parseFloat(location.lng)},
      map: map,
      title: location.nombre // Añadir el título al marcador
    });
  
    var infoWindowContent = `
    <div style="background-color: #fff; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); padding: 10px; max-width: 300px;">
      <h2 style="font-size: 18px; margin-bottom: 10px;">${location.nombre}</h2>
      <p style="margin-bottom: 5px;"><strong>DNI:</strong> ${location.dni}</p>
      <p style="margin-bottom: 5px;"><strong>Correo:</strong> ${location.correo}</p>
      <p style="margin-bottom: 5px;"><strong>Dirección:</strong> ${location.direccion}</p>
      <p style="margin-bottom: 5px;"><strong>Teléfono:</strong> ${location.telefono}</p>
      <p style="margin-bottom: 5px;"><strong>Consulta Médica:</strong> ${location.consulta_medica}</p>
      <p style="margin-bottom: 5px;"><strong>Estado:</strong> ${location.estado}</p>
      <p style="margin-bottom: 5px;"><strong>Fecha de Cita:</strong> ${location.fecha_cita}</p>
      <!-- Agregar más campos según sea necesario -->
    </div>
  `;
  
    var infoWindow = new google.maps.InfoWindow({
      content: infoWindowContent
    });
  
    marker.addListener('click', function() {
      infoWindow.open(map, marker);
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



    // El token JWT
    const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzOTkiLCJuYW1lIjoiY2FybG9zTW9yaTI4IiwiZW1haWwiOiJjZWdtY2FybG9zOTg3QGdtYWlsLmNvbSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6ImNvbnN1bHRvciJ9.lOQWVQhrxupKVNlJLRu2Xdsai7mfPuDD3Vcc-lixqP8';

    // URL base de la API
    const baseUrl = 'https://api.factiliza.com/pe/v1/';

    // Función para realizar la consulta a la API usando AJAX
    function consultarDNI(dni) {
        // Construye la URL de la API
        const url = `${baseUrl}dni/info/${dni}`;

        // Realiza la solicitud AJAX
        $.ajax({
            url: url,
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            success: function(datos) {
                mostrarResultado(datos);
            },
            error: function(xhr, status, error) {
                $('#resultado').text(`Error: ${xhr.status} - ${xhr.statusText}`);
            }
        });
    }

    // Añade un evento de envío al formulario
    $('#consultaForm').on('submit', function(event) {
        // Evita el envío del formulario por defecto
        event.preventDefault();

        // Obtiene el valor del campo DNI
        const dni = $('#dniRellenar').val();

        // Llama a la función de consulta con el DNI como valor
        consultarDNI(dni);
    });

    // Función para mostrar los resultados de la consulta
    function mostrarResultado(datos) {
        if (datos.status === 200 && datos.message === 'Exito') {
            const data = datos.data;

            // Eliminar las comas del nombre
            const nombreSinComas = data.nombre_completo.replace(/,/g, '');

            // Actualizar campos específicos del formulario
            $('#dni').val(data.numero);
            $('#nombre').val(nombreSinComas);
            $('#direccion').val(data.direccion_completa);

        } else {
            $('#resultado').text(`Error: No se encontró información o hubo un problema con la consulta.`);
        }
    }