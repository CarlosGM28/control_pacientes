import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime
import pyrebase
import google.generativeai as genai

app = Flask(__name__)

# Configurar la clave secreta de sesión
app.secret_key = 'tu_clave_secreta_aquí'

# Configuración de Pyrebase
config = {
    "apiKey": "AIzaSyD6GxCq4msYsbtQSRu5IIlyCKYpkM6MEq8",
    "authDomain": "iapython-950bf.firebaseapp.com",
    "databaseURL": "https://iapython-950bf-default-rtdb.firebaseio.com",
    "projectId": "iapython-950bf",
    "storageBucket": "iapython-950bf.appspot.com",
    "messagingSenderId": "157402200715",
    "appId": "1:157402200715:web:3b8526783cd9356ee4728e",
    "measurementId": "G-ECZM8MK1DF"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# Decorador para verificar la autenticación del usuario
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('index'))  # Redirigir al usuario a la página de inicio si no está autenticado
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prueba')
def prueba():
    return render_template('prueba.html')

@app.route('/registrar_personal', methods=['POST'])
def signup():

    tipo_alerta = 'success'
    mensaje_alerta = 'Personal registrado correctamente'
    tipo_registro = 'personal'

    nombre = request.form['nombre']
    dni = request.form['dni']
    telefono = request.form['telefono']
    especialidad = request.form['especialidad']
    genero = request.form['genero']
    rol = request.form['rol']
    email = request.form['email']
    password = request.form['password']

    try:

        hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Crear usuario con correo electrónico y contraseña
        user = auth.create_user_with_email_and_password(email, password)

        # Agregar datos de personal a la colección "personal" en la base de datos
        db.child('personal').child(dni).set({
            'nombre': nombre,
            'dni': dni,
            'especialidad': especialidad,
            'telefono': telefono,
            'genero': genero,
            'rol': rol,
            'email': email,
            'hora_actual': hora_actual
        })

        return redirect(url_for('mostrar_alerta', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, tipo_registro=tipo_registro))
    except Exception as e:
        tipo_alerta = 'danger'
        mensaje_alerta = 'Error al registrar al personal: {}'.format(str(e))
        return redirect(url_for('mostrar_alerta', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, tipo_registro=tipo_registro))

@app.route('/registrar_paciente', methods=['POST'])
def pacientes():

    tipo_alerta = 'success'
    mensaje_alerta = 'Paciente registrado correctamente'
    tipo_registro = 'paciente'
    estado = 'Pendiente'

    nombre = request.form['nombre']
    dni = request.form['dni']
    fecha_nacimiento = request.form['fecha_nacimiento']
    genero = request.form['genero']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    correo = request.form['correo']
    consulta_medica = request.form['consulta_medica']
    especialista = request.form['especialista']
    presion_arterial = request.form['presion_arterial']
    saturacion = request.form['saturacion']
    temperatura = request.form['temperatura']
    peso = request.form['peso']
    frecuencia_respiratoria = request.form['frecuencia_respiratoria']
    talla = request.form['talla']
    frecuencia_cardiaca = request.form['frecuencia_cardiaca']
    imc = request.form['imc']
    fecha_cita = request.form['fecha_cita']
    latitud = request.form['latitud']
    logitud = request.form['logitud']

    try:

        hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Generar una clave única para cada registro dentro de la clave 'dni'
        new_patient_ref = db.child("Pacientes").child(dni).push({
            'nombre': nombre,
            'dni': dni,
            'fecha_nacimiento': fecha_nacimiento,
            'genero': genero,
            'direccion': direccion,
            'telefono': telefono,
            'correo': correo,
            'consulta_medica': consulta_medica,
            'especialista': especialista,
            'presion_arterial': presion_arterial,
            'saturacion': saturacion,
            'temperatura': temperatura,
            'peso': peso,
            'frecuencia_respiratoria': frecuencia_respiratoria,
            'talla': talla,
            'frecuencia_cardiaca': frecuencia_cardiaca,
            'imc': imc,
            'hora_registro': hora_actual,
            'fecha_cita': fecha_cita,
            'estado': estado,
            'lat': latitud,
            'lng': logitud

        })

        return redirect(url_for('mostrar_alerta', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, tipo_registro=tipo_registro))

    except Exception as e:
        tipo_alerta = 'danger'
        mensaje_alerta = 'Error al registrar al paciente: {}'.format(str(e))
        return redirect(url_for('mostrar_alerta', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, tipo_registro=tipo_registro))


@app.route('/mostrar_alerta/<tipo_alerta>/<mensaje_alerta>/<tipo_registro>')
def mostrar_alerta(tipo_alerta, mensaje_alerta, tipo_registro):
    # Obtener el correo electrónico del usuario autenticado desde la sesión
    user_email = session.get('user_email')

    # Si el usuario no ha iniciado sesión, redirigirlo al inicio de sesión
    if not user_email:
        return redirect('/login')
        
    if tipo_registro == 'personal':
        return render_template('vistas/register.html', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, user_email=user_email)
    elif tipo_registro == 'paciente':
        return render_template('principal.html', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, user_email=user_email)

@app.route('/registros_pacientes', methods=['GET'])
def regis_paciente():
    # Obtener todos los registros de la tabla 'Pacientes'
    registros_pacientes = db.child("Pacientes").get().val()

    # Lista para almacenar los datos de los pacientes
    datos_pacientes = []

    # Iterar sobre los registros de pacientes
    for dni, paciente_data in registros_pacientes.items():
        # Verificar si paciente_data es un diccionario
        if isinstance(paciente_data, dict):
            # Iterar sobre los elementos del diccionario paciente_data
            for key, paciente in paciente_data.items():
                # Crear un diccionario para almacenar los datos de cada paciente
                datos_paciente = {
                    'nombre': paciente.get('nombre', ''),
                    'dni': paciente.get('dni', ''),
                    'consulta_medica': paciente.get('consulta_medica', ''),
                    'correo': paciente.get('correo', ''),
                    'direccion': paciente.get('direccion', ''),
                    'especialista': paciente.get('especialista', ''),
                    'fecha_nacimiento': paciente.get('fecha_nacimiento', ''),
                    'frecuencia_cardiaca': paciente.get('frecuencia_cardiaca', ''),
                    'frecuencia_respiratoria': paciente.get('frecuencia_respiratoria', ''),
                    'genero': paciente.get('genero', ''),
                    'hora_registro': paciente.get('hora_registro', ''),
                    'fecha_cita': paciente.get('fecha_cita', ''),
                    'imc': paciente.get('imc', ''),
                    'peso': paciente.get('peso', ''),
                    'presion_arterial': paciente.get('presion_arterial', ''),
                    'saturacion': paciente.get('saturacion', ''),
                    'talla': paciente.get('talla', ''),
                    'telefono': paciente.get('telefono', ''),
                    'temperatura': paciente.get('temperatura', ''),
                    'estado': paciente.get('estado', ''),
                    'lat': paciente.get('lat', ''),
                    'lng': paciente.get('lng', '')
                }
                datos_pacientes.append(datos_paciente)
        else:
            # Manejar el caso donde paciente_data no es un diccionario
            print(f"Los datos del paciente con DNI {dni} no son válidos.")

    # Devolver los datos de los pacientes como JSON
    return jsonify({"datos": datos_pacientes})


@app.route('/editar_paciente', methods=['POST'])
def editar_paciente():
        # Obtener el correo electrónico del usuario autenticado desde la sesión
    user_email = session.get('user_email')

    # Si el usuario no ha iniciado sesión, redirigirlo al inicio de sesión
    if not user_email:
        return redirect('/login')
    
    tipo_alerta = 'success'
    mensaje_alerta = 'Paciente editado correctamente'
    tipo_registro = 'paciente'
    if request.method == 'POST':
        # Obtener los datos del formulario de edición
        dni = request.form['dniEdit']
        hora_registro = request.form['horaRegistroEdit']

        # Realizar una consulta en la base de datos utilizando el DNI
        paciente_data = db.child("Pacientes").child(dni).get().val()

        if paciente_data:
            # Obtener la clave autogenerada del registro que se va a editar
            registro_key = None
            for key, paciente in paciente_data.items():
                if paciente.get("hora_registro") == hora_registro:
                    registro_key = key
                    break

            if registro_key:
                # Obtener los demás datos del formulario
                nombre = request.form['nombreEdit']
                fecha_nacimiento = request.form['fechaNacimientoEdit']
                genero = request.form['generoEdit']
                correo = request.form['correoEdit']
                telefono = request.form['telefonoEdit']
                direccion = request.form['direccionEdit']
                consulta_medica = request.form['consultaMedicaEdit']
                especialista = request.form['especialistaEdit']
                presion_arterial = request.form['presionArterialEdit']
                saturacion = request.form['saturacionEdit']
                temperatura = request.form['temperaturaEdit']
                peso = request.form['pesoEdit']
                frecuencia_respiratoria = request.form['frecuenciaRespiratoriaEdit']
                talla = request.form['tallaEdit']
                frecuencia_cardiaca = request.form['frecuenciaCardiacaEdit']
                imc = request.form['imcEdit']
                hora_registro = request.form['horaRegistroEdit']
                estado = request.form['estadoEdit']
                lat = request.form['latEditar']
                lng = request.form['lngEditar']
                # Crear un diccionario con los datos actualizados
                datos_actualizados = {
                    "nombre": nombre,
                    "fecha_nacimiento": fecha_nacimiento,
                    "genero": genero,
                    "correo": correo,
                    "telefono": telefono,
                    "direccion": direccion,
                    "consulta_medica": consulta_medica,
                    "especialista": especialista,
                    "presion_arterial": presion_arterial,
                    "saturacion": saturacion,
                    "temperatura": temperatura,
                    "peso": peso,
                    "frecuencia_respiratoria": frecuencia_respiratoria,
                    "talla": talla,
                    "frecuencia_cardiaca": frecuencia_cardiaca,
                    "imc": imc,
                    "hora_registro": hora_registro,
                    'estado': estado,
                    'lat': lat,
                    'lng': lng
                }

                # Actualizar los datos en Firebase utilizando la clave autogenerada
                db.child("Pacientes").child(dni).child(registro_key).update(datos_actualizados)

                # Devolver una respuesta JSON indicando el éxito de la operación
                return redirect(url_for('mostrar_alerta', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, tipo_registro=tipo_registro, user_email=user_email))
            else:
                tipo_alerta = 'danger'
                mensaje_alerta = 'Error al editar al paciente'
                return redirect(url_for('mostrar_alerta', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, tipo_registro=tipo_registro, user_email=user_email))


@app.route('/eliminar_paciente', methods=['POST'])
def eliminar_paciente():
    # Obtener el correo electrónico del usuario autenticado desde la sesión
    user_email = session.get('user_email')

    # Si el usuario no ha iniciado sesión, redirigirlo al inicio de sesión
    if not user_email:
        return redirect('/login')
    tipo_alerta = 'success'
    mensaje_alerta = 'Paciente eliminado correctamente'
    tipo_registro = 'paciente'

    if request.method == 'POST':
        # Obtener los datos del formulario para eliminar
        dni = request.form['dniDelete']
        hora_registro = request.form['horaRegistroDelete']

        # Realizar una consulta en la base de datos utilizando el DNI
        paciente_data = db.child("Pacientes").child(dni).get().val()

        if paciente_data:
            # Obtener la clave autogenerada del registro que se va a eliminar
            registro_key = None
            for key, paciente in paciente_data.items():
                if paciente.get("hora_registro") == hora_registro:
                    registro_key = key
                    break

            if registro_key:
                # Eliminar el registro de la base de datos
                db.child("Pacientes").child(dni).child(registro_key).remove()

                # Devolver una respuesta JSON indicando el éxito de la operación
                return redirect(url_for('mostrar_alerta', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, tipo_registro=tipo_registro,user_email=user_email))
            else:
                tipo_alerta = 'danger'
                mensaje_alerta = 'Error al eliminar al paciente'
                return redirect(url_for('mostrar_alerta', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, tipo_registro=tipo_registro,user_email=user_email))
        else:
            tipo_alerta = 'danger'
            mensaje_alerta = 'Error al eliminar al paciente: No se encontraron registros para el DNI proporcionado'
            return redirect(url_for('mostrar_alerta', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, tipo_registro=tipo_registro,user_email=user_email))
    else:
        tipo_alerta = 'danger'
        mensaje_alerta = 'Error al eliminar al paciente: Método no permitido'
        return redirect(url_for('mostrar_alerta', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, tipo_registro=tipo_registro,))


@app.route('/registros_pacientes_medicos', methods=['GET'])
def registro_personal_madico():
    # Obtener todos los registros de la tabla 'Pacientes'
    registros_personal = db.child("personal").get().val()

    # Lista para almacenar los datos de los pacientes
    datos_personal = []

    # Iterar sobre los registros de pacientes
    for dni, personal_data in registros_personal.items():
        # Crear un diccionario para almacenar los datos de cada paciente
        datos_personal_medico = {
            'nombre': personal_data.get('nombre', ''),
            'dni': personal_data.get('dni', ''),
            'especialidad': personal_data.get('especialidad', ''),
            'telefono': personal_data.get('telefono', ''),
            'genero': personal_data.get('genero', ''),
            'rol': personal_data.get('rol', ''),
            'email': personal_data.get('email', ''),
            'hora_actual': personal_data.get('hora_actual', '')
        }
        datos_personal.append(datos_personal_medico)

    # Devolver los datos de los pacientes como JSON
    return jsonify({"datos": datos_personal})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['correo']
        password = request.form['password']

        try:
            # Attempt to sign in with the provided email and password
            user_cred = auth.sign_in_with_email_and_password(email, password)

            # Get the authenticated user's email
            user_email = user_cred['email']

            # Store the user's email in the session
            session['user_email'] = user_email

            # Redirect the user to the main page
            return redirect('/principal')
        except Exception as e:
            # Default alert type and message
            tipo_alerta = 'danger'
            mensaje_alerta = 'Error desconocido'

            error_str = str(e)
            if "EMAIL_NOT_FOUND" in error_str:
                mensaje_alerta = 'Email Incorrecto'
            elif "INVALID_PASSWORD" in error_str:
                mensaje_alerta = 'Contraseña Incorrecta'
            elif "USER_DISABLED" in error_str:
                mensaje_alerta = 'Cuenta Deshabilitada'
            else:
                mensaje_alerta = 'Correo o Contraseña es Incorrecta'
            # Render the login template with the error message
            return render_template('index.html', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta)

    # If the request is GET, render the login template
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()  # Destruye la sesión
    return redirect(url_for('index'))  # Redirige al usuario a la página de inicio de sesión o a otra página

@app.route('/ia_medic', methods=['GET', 'POST'])
def iamedic():
    # Asigna tu clave de API a una variable de entorno
    os.environ['API_KEY'] = 'AIzaSyDNsuMqMk70F73lY_1SQKrKHbXhJn0PLcY'

    # Configura la clave de API desde la variable de entorno
    api_key = os.environ.get('API_KEY')
    if not api_key:
        return "API_KEY no encontrada en las variables de entorno."

    genai.configure(api_key=api_key)

    # Obtiene la ruta absoluta del archivo palabras_claves.txt
    palabras_claves_file = os.path.join(os.path.dirname(__file__), 'palabras_claves.txt')

    # Leer palabras clave desde el archivo
    try:
        with open(palabras_claves_file, "r") as file:
            # Leer las líneas y eliminar comillas y espacios en blanco
            palabras_clave = [line.strip().strip('"') for line in file.read().split(",")]
    except FileNotFoundError:
        palabras_clave = []
        return "Error: El archivo palabras_claves.txt no se encontró."

    # Creación del modelo generativo
    model = genai.GenerativeModel('gemini-pro')

    if request.method == 'POST':
        pregunta_usuario = request.form['pregunta']
        if any(keyword in pregunta_usuario.lower() for keyword in palabras_clave):
            response = model.generate_content(f"Pregunta: {pregunta_usuario}")
            lines = response.text.split('\n')
            formatted_lines = []
            ul_open = False
            strong_open = False

            for line in lines:
                if line.startswith('*'):
                    if not ul_open:
                        formatted_lines.append('<ul>')
                        ul_open = True
                    line = line.replace('*', '').strip()
                    if '**' in line:
                        if not strong_open:
                            formatted_lines.append('<strong>')
                            strong_open = True
                        line = line.replace('**', '').strip()
                        formatted_lines.append(f'<li>{line}</li>')
                        formatted_lines.append('</strong>')
                        strong_open = False
                    else:
                        formatted_lines.append(f'<li>{line}</li>')
                elif ul_open:
                    formatted_lines.append('</ul>')
                    ul_open = False
                elif '**' in line:
                    if not strong_open:
                        formatted_lines.append('<strong>')
                        strong_open = True
                    line = line.replace('**', '').strip()
                    formatted_lines.append(f'<p>{line}</p>')
                    formatted_lines.append('</strong>')
                    strong_open = False
                else:
                    formatted_lines.append(f'<p>{line}</p>')

            respuesta = ''.join(formatted_lines)
        else:
            respuesta = "Lo siento, esta pregunta no está relacionada con la medicina."
        return render_template('vistas/ia_medic.html', respuesta=respuesta)
    elif request.method == 'GET':
        return render_template('vistas/ia_medic.html')

@app.route('/principal')
def principal():
    # Obtener el correo electrónico del usuario autenticado desde la sesión
    user_email = session.get('user_email')

    # Si el usuario no ha iniciado sesión, redirigirlo al inicio de sesión
    if not user_email:
        return redirect('/login')

    # Renderizar la plantilla principal y pasar el correo electrónico del usuario
    return render_template('principal.html', user_email=user_email)

@app.route('/personal')
def paciente():
            # Obtener el correo electrónico del usuario autenticado desde la sesión
    user_email = session.get('user_email')

    # Si el usuario no ha iniciado sesión, redirigirlo al inicio de sesión
    if not user_email:
        return redirect('/login')

    # Renderizar la plantilla principal y pasar el correo electrónico del usuario
    return render_template('vistas/register.html', user_email=user_email)

@app.route('/medico_bot')
def medicobot():
    # Obtener el correo electrónico del usuario autenticado desde la sesión
    user_email = session.get('user_email')

    # Si el usuario no ha iniciado sesión, redirigirlo al inicio de sesión
    if not user_email:
        return redirect('/login')

    # Renderizar la plantilla principal y pasar el correo electrónico del usuario
    return render_template('vistas/ia_medic.html', user_email=user_email)

@app.route('/registro_reniec')
def ciudadano():
    # Obtener el correo electrónico del usuario autenticado desde la sesión
    user_email = session.get('user_email')

    # Si el usuario no ha iniciado sesión, redirigirlo al inicio de sesión
    if not user_email:
        return redirect('/login')

    # Renderizar la plantilla principal y pasar el correo electrónico del usuario
    return render_template('vistas/reniec.html', user_email=user_email)

@app.route('/citas_medicas')
def citas():
    # Obtener el correo electrónico del usuario autenticado desde la sesión
    user_email = session.get('user_email')

    # Si el usuario no ha iniciado sesión, redirigirlo al inicio de sesión
    if not user_email:
        return redirect('/login')

    # Renderizar la plantilla principal y pasar el correo electrónico del usuario
    return render_template('vistas/citas.html', user_email=user_email)

@app.route('/mapas_pacientes')
def mapas():
    # Obtener el correo electrónico del usuario autenticado desde la sesión
    user_email = session.get('user_email')
    tipo_alerta = 'success'
    mensaje_alerta = 'Paciente editado correctamente'
    
    # Si el usuario no ha iniciado sesión, redirigirlo al inicio de sesión
    if not user_email:
        return redirect('/login')
    

    
    return render_template('vistas/mapa_pacientes.html', user_email=user_email)

@app.route('/pruebamapas')
def mapas_prueba():

    return render_template('vistas/mapas_prueba.html')

@app.route('/consultas')
def reniec():
    return render_template('vistas/reniec.html')

if __name__ == '__main__':
    app.run(debug=True)