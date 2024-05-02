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
                    {
                        // Columna de botones
                        data: null,
                        render: function(data, type, row) {
                            return '<button class="btn btn-info ver-detalles" style="margin-right: 5px;"><i class="fas fa-eye"></i></button>' +
                                '<button class="btn btn-warning editar" style="margin-right: 5px;"><i class="fas fa-pencil-alt"></i></button>' +
                                '<button class="btn btn-danger eliminar" style="margin-right: 5px;"><i class="fas fa-trash-alt"></i></button>';
                        }
                    }
                ],
                columnDefs: [
                    {
                        targets: -1,
                        orderable: false,
                        searchable: false
                    }
                ]
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
