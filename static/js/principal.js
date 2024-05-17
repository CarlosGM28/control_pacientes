$(document).ready(function() {
    $.ajax({
        url: '/registros_pacientes',
        type: "GET",
        success: function(response) {
            console.log(response);
            $('#data_table').DataTable({
                pageLength: 10,
                data: response["datos"],
                columns: [
                    { data: 'nombre' },
                    { data: 'dni' },
                    { data: 'correo' },
                    { data: 'direccion' },
                    { data: 'telefono' },
                    { data: 'genero' },
                    { data: 'fecha_nacimiento' },
                    { data: 'hora_registro' },
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
                    },
                    { data: 'consulta_medica', visible: false },
                    { data: 'especialista', visible: false },
                    { data: 'frecuencia_cardiaca', visible: false },
                    { data: 'frecuencia_respiratoria', visible: false },
                    { data: 'imc', visible: false },
                    { data: 'peso', visible: false },
                    { data: 'presion_arterial', visible: false },
                    { data: 'saturacion', visible: false },
                    { data: 'talla', visible: false },
                    { data: 'temperatura', visible: false }
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
                // Mostrar detalles del paciente en el modal
                $('#nombrePaciente').text(data.nombre);
                $('#dniPaciente').text(data.dni);
                $('#correoPaciente').text(data.correo);
                $('#direccionPaciente').text(data.direccion);
                $('#telefonoPaciente').text(data.telefono);
                $('#generoPaciente').text(data.genero);
                $('#fechaNacimientoPaciente').text(data.fecha_nacimiento);
                $('#horaRegistroPaciente').text(data.hora_registro);
                $('#consultaMedicaPaciente').text(data.consulta_medica);
                $('#especialistaPaciente').text(data.especialista);
                $('#frecuenciaCardiacaPaciente').text(data.frecuencia_cardiaca);
                $('#frecuenciaRespiratoriaPaciente').text(data.frecuencia_respiratoria);
                $('#imcPaciente').text(data.imc);
                $('#pesoPaciente').text(data.peso);
                $('#presionArterialPaciente').text(data.presion_arterial);
                $('#saturacionPaciente').text(data.saturacion);
                $('#tallaPaciente').text(data.talla);
                $('#temperaturaPaciente').text(data.temperatura);
                $('#detallesModal').modal('show');
            });

            // Manejar clics en los botones de editar
            $('#data_table tbody').on('click', '.editar', function() {
                var data = $('#data_table').DataTable().row($(this).parents('tr')).data();
                // Lógica para editar
                // Actualizar los campos del formulario en el modal con los datos del paciente
                $('#nombreEdit').val(data.nombre);
                $('#dniEdit').val(data.dni);
                $('#correoEdit').val(data.correo);
                $('#direccionEdit').val(data.direccion);
                $('#telefonoEdit').val(data.telefono);
                $('#generoEdit').val(data.genero);
                $('#fechaNacimientoEdit').val(data.fecha_nacimiento);
                $('#horaRegistroEdit').val(data.hora_registro);
                $('#consultaMedicaEdit').val(data.consulta_medica);
                $('#especialistaEdit').val(data.especialista);
                $('#frecuenciaCardiacaEdit').val(data.frecuencia_cardiaca);
                $('#frecuenciaRespiratoriaEdit').val(data.frecuencia_respiratoria);
                $('#imcEdit').val(data.imc);
                $('#pesoEdit').val(data.peso);
                $('#presionArterialEdit').val(data.presion_arterial);
                $('#saturacionEdit').val(data.saturacion);
                $('#tallaEdit').val(data.talla);
                $('#temperaturaEdit').val(data.temperatura);
                // Mostrar el modal para editar los datos
                $('#editarModal').modal('show');
            });

            // Manejar clics en los botones de eliminar
            $('#data_table tbody').on('click', '.eliminar', function() {
                var data = $('#data_table').DataTable().row($(this).parents('tr')).data();
                $('#dniDelete').val(data.dni);
                $('#horaRegistroDelete').val(data.hora_registro);
                // Mostrar el modal para confirmar la eliminación
                $('#confirmarEliminarModal').modal('show');
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