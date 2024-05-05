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
            'hora_registro': hora_actual

        })
        
        return redirect(url_for('mostrar_alerta', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, tipo_registro=tipo_registro))

    except Exception as e:
        tipo_alerta = 'danger'
        mensaje_alerta = 'Error al registrar al paciente: {}'.format(str(e))
        return redirect(url_for('mostrar_alerta', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta, tipo_registro=tipo_registro))


@app.route('/mostrar_alerta/<tipo_alerta>/<mensaje_alerta>/<tipo_registro>')
def mostrar_alerta(tipo_alerta, mensaje_alerta, tipo_registro):
    if tipo_registro == 'personal':
        return render_template('vistas/register.html', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta)
    elif tipo_registro == 'paciente':
        return render_template('principal.html', tipo_alerta=tipo_alerta, mensaje_alerta=mensaje_alerta)       

@app.route('/registros_pacientes', methods=['GET'])
def regis_paciente():
    # Obtener todos los registros de la tabla 'Pacientes'
    registros_pacientes = db.child("Pacientes").get().val()
    
    # Lista para almacenar los datos de los pacientes
    datos_pacientes = []

    # Iterar sobre los registros de pacientes
    for dni, paciente_data in registros_pacientes.items():
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
                'imc': paciente.get('imc', ''),
                'peso': paciente.get('peso', ''),
                'presion_arterial': paciente.get('presion_arterial', ''),
                'saturacion': paciente.get('saturacion', ''),
                'talla': paciente.get('talla', ''),
                'telefono': paciente.get('telefono', ''),
                'temperatura': paciente.get('temperatura', '')
            }
            datos_pacientes.append(datos_paciente)
    
    # Devolver los datos de los pacientes como JSON
    return jsonify({"datos":datos_pacientes})

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
            # Intentar iniciar sesión con el correo electrónico y la contraseña proporcionados
            user_cred = auth.sign_in_with_email_and_password(email, password)

            # Obtener el correo electrónico del usuario autenticado
            user_email = user_cred['email']

            # Almacenar el correo electrónico del usuario en la sesión de forma global
            session['user_email'] = user_email

            # Redirigir al usuario a la página principal
            return redirect('/principal')
        except Exception as e:
            # Si ocurre un error de autenticación, mostrar un mensaje de error al usuario
            error_message = str(e)
            print('Error de autenticación:', error_message)
            return render_template('index.html', error=error_message)

    # Si la solicitud es GET, renderizar la plantilla de inicio de sesión
    return render_template('index.html')

@app.route('/ia_medic', methods=['GET', 'POST'])
def iamedic():
        # Asigna tu clave de API a una variable de entorno
        os.environ['API_KEY'] = 'AIzaSyDNsuMqMk70F73lY_1SQKrKHbXhJn0PLcY'

        # Configura la clave de API desde la variable de entorno
        api_key = os.environ.get('API_KEY')
        if not api_key:
            return "API_KEY no encontrada en las variables de entorno."

        genai.configure(api_key=api_key)

        # Leer palabras clave desde el archivo
        try:
            with open("palabras_claves.txt", "r") as file:
                # Leer las líneas y eliminar comillas y espacios en blanco
                palabras_clave = [line.strip().strip('"') for line in file.read().split(",")]
        except FileNotFoundError:
            return "Error: El archivo palabras_clave.txt no se encontró."

        # Creación del modelo generativo
        model = genai.GenerativeModel('gemini-pro')

        if request.method == 'POST':
            pregunta_usuario = request.form['pregunta']
            if any(keyword in pregunta_usuario.lower() for keyword in palabras_clave):
                response = model.generate_content(f"Pregunta: {pregunta_usuario}")
                respuesta = response.text
            else:
                respuesta = "Lo siento, esta pregunta no está relacionada con la medicina."
            return render_template('vistas/ia_medic.html', respuesta=respuesta)
        elif request.method == 'GET':
            return render_template('vistas/ia_medic.html')

@app.route('/logout')
def logout():
    # Eliminar el ID de usuario de la sesión
    session.pop('user_id', None)

    # Redirigir al usuario a la página de inicio
    return redirect(url_for('index'))

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


if __name__ == '__main__':
    app.run(debug=True)