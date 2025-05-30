from flask import Flask, render_template, request, redirect, session, url_for, jsonify, flash
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# añade una clave secreta para la sesión
app.secret_key = "miclavesecreta123"

API_BASE_URL = "http://localhost:5001"
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "IMAGES", "perfiles")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "svg", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Página principal: Login
@app.route("/")
def index():
    # Obtener usuarios desde la API
    response = requests.get(f"{API_BASE_URL}/auth/users")
    usuarios = response.json() if response.status_code == 200 else []
    return render_template("login.html")

# Página Principal de Inicio
@app.route('/inicio')
def inicio():
    usuario = session.get("usuario")
    if usuario:
        # Obtener los IDs de las actividades inscritas del usuario
        response = requests.get(f"{API_BASE_URL}/activity/user/{usuario['idusuario']}/subscriptions")
        actividad_ids = response.json() if response.status_code == 200 else []

        # Obtener los detalles de todas las actividades en una sola solicitud
        detalle_response = requests.post(
            f"{API_BASE_URL}/activity/details",
            json=actividad_ids
        )
        actividades = detalle_response.json() if detalle_response.status_code == 200 else []

        # Agregar las actividades al usuario
        usuario["actividades"] = actividades
        session["usuario"] = usuario  # Actualizar la sesión

    return render_template('inicio.html', usuario=usuario)



@app.route("/modal_Usuario")
def modal_usuario():
    usuario = session.get("usuario")
    if not usuario:
        flash("Debes iniciar sesión para ver tu perfil.", "danger")
        return redirect(url_for("index"))
    return render_template("modalUsuario.html", usuario=usuario)

# ...existing code...
@app.route("/RecuperarContraseña")
def recuperar_contraseña():
    return render_template("RecuperarConstraseña.html")


# Dashboard del usuario
@app.route("/dashboard") 
def dashboard():
    # Obtener el ID del usuario desde la sesión
    usuario = session.get("usuario")
    if not usuario:
        flash("Debes iniciar sesión para ver las actividades.", "danger")
        return redirect(url_for("index"))

    # Llamar al endpoint de la API para obtener todas las actividades
    response = requests.get(f"{API_BASE_URL}/activity/all")
    actividades = response.json() if response.status_code == 200 else []

    # Llamar al endpoint de la API para obtener las actividades en las que el usuario está inscrito
    usuario_id = usuario["idusuario"]
    response_inscripciones = requests.get(f"{API_BASE_URL}/activity/user/{usuario_id}/subscriptions")
    inscripciones = response_inscripciones.json() if response_inscripciones.status_code == 200 else []

    # Obtener los participantes de todas las actividades
    for actividad in actividades:
        participantes_response = requests.get(f"{API_BASE_URL}/activity/{actividad['idactividad']}/participantes")
        participantes = participantes_response.json() if participantes_response.status_code == 200 else []

        # Contador de participantes
        actividad["num_participantes"] = len(participantes)

        # Crear un array con solo los nombres de los usuarios
        nombres_participantes = [participante["nombre"] for participante in participantes]
        actividad["participantes"] = nombres_participantes  # Asignar solo los nombres
        print(f"Actividad {actividad['idactividad']} participantes: {actividad['participantes']}")

    return render_template("dashboard.html", actividades=actividades, inscripciones=inscripciones, usuario=usuario)


@app.route("/inscribirse/<int:actividad_id>", methods=["POST"])
def inscribirse(actividad_id):
    # Obtener el ID del usuario desde la sesión
    usuario_id = session.get("usuario", {}).get("idusuario")
    if not usuario_id:
        flash("Debes iniciar sesión para inscribirte en una actividad.", "danger")
        return redirect(url_for("index"))

    # Enviar la solicitud a la API
    response = requests.post(
        f"{API_BASE_URL}/activity/{actividad_id}/subscribe",
        json=usuario_id
    )

    # Manejar la respuesta de la API
    if response.status_code == 200:
        flash("¡Inscripción exitosa!", "success")
    else:
        error_message = response.json().get("message", "Error al inscribirse")
        flash(error_message, "danger")

    return redirect(url_for("dashboard"))


@app.route("/desinscribirse/<int:actividad_id>", methods=["POST"])
def desinscribirse(actividad_id):
    # Obtener el ID del usuario desde la sesión
    usuario_id = session.get("usuario", {}).get("idusuario")
    if not usuario_id:
        flash("Debes iniciar sesión para borrarte de una actividad.", "danger")
        return redirect(url_for("index"))

    # Enviar la solicitud a la API
    try:
        response = requests.delete(
            f"{API_BASE_URL}/activity/{actividad_id}/unsubscribe",
            json=usuario_id
        )
        
        # Manejar la respuesta de la API
        if response.status_code == 200:
            flash(response.json().get("message", "¡Te has borrado de la actividad con éxito!"), "success")
        else:
            error_message = response.json().get("message", "Error al borrarse de la actividad")
            flash(error_message, "danger")
    except Exception as e:
        flash("Error al conectar con la API.", "danger")

    return redirect(url_for("dashboard"))


@app.route("/crear_actividad", methods=["POST"])
def crear_actividad():
    # Obtener los datos del formulario enviados desde el frontend
    data = {
        "Nombre": request.form.get("nombre"),
        "Descripcion": request.form.get("descripcion"),
        "Tipo": request.form.get("tipo"),
        "Fecha": request.form.get("fecha"),
        "Hora": request.form.get("hora"),
        "Lugar": request.form.get("lugar"),
        "Duracion": request.form.get("duracion")
    }
        #"IdOrganizador": request.form.get("idOrganizador"),

    # Enviar los datos al backend
    response = requests.post(f"{API_BASE_URL}/activity/create", json=data)

     # Manejar la respuesta del backend
    if response.status_code == 200:
        flash("¡Actividad creada exitosamente!", "success")
    else:
        flash(response.json().get("message", "Error al crear la actividad"), "danger")
    return redirect(url_for("dashboard"))


@app.route("/sobrenosotros")
def sobre_nosotros():
    usuario = session.get("usuario")
    return render_template("sobrenosotros.html", usuario=usuario)




@app.route("/tienda")
def tienda():
    usuario = session.get("usuario")
    return render_template("tienda.html", usuario=usuario)


# Procesa el login
@app.route("/login", methods=["POST"])
def login():
    data = {
        "username": request.form["username"],
        "password": request.form["password"]
    }
    response = requests.post(f"{API_BASE_URL}/auth/login", json=data)
    if response.status_code == 200:
        usuario = response.json().get("usuario")
        
        # Guardar todo en la sesión
        session["usuario"] = {
            "idusuario": usuario["idusuario"],
            "username": usuario["username"],
            "password": data["password"],
            "email": usuario.get("email"),
            "telefono": usuario.get("telefono"),
            "pais": usuario.get("pais"),
            "edad": usuario.get("edad"),
            "foto": usuario.get("foto", "default-avatar.svg")
        }
        
        return redirect(url_for("inicio"))
    elif response.status_code == 401:
        flash("Usuario o contraseña incorrectos", "danger")
        return render_template("login.html")
    else:
        return f"Error en la conexión con la API: {response.text}", response.status_code
    

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        # Obtener datos del formulario
        nombre = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        telefono = request.form.get("telefono")
        pais = request.form.get("pais")
        edad = request.form.get("edad")

        # Construir payload para enviar a la API
        data = {
            "username": nombre,
            "email": email,
            "password": password,
            "telefono": telefono,
            "pais": pais,
            "edad": int(edad),
            "foto": "default-avatar.svg" 
        }

        response = requests.post(f"{API_BASE_URL}/auth/registro", json=data)

        if response.status_code == 200:
            flash("¡Usuario registrado correctamente!", "success")
            return redirect(url_for("index"))  # Redirige a inicio
        elif response.status_code == 409:
            flash("Ese correo electrónico ya está en uso. Intenta con otro.", "danger")
            return render_template("registro.html")
        else:
            return f"Error al registrar usuario: {response.text}", response.status_code

    return render_template("registro.html")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/subir_foto", methods=["POST"])
def subir_foto():

    if "foto" not in request.files:
        flash("No se seleccionó ninguna imagen", "danger")
        return redirect(url_for("inicio"))

    file = request.files["foto"]

    if file.filename == "":
        flash("Nombre de archivo vacio", "danger")
        return redirect(url_for("inicio"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])


        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        usuario = session.get("usuario")
        usuario["foto"] = filename
        
        # Construir el payload con toda la información del usuario
        usuarioCompleto = {
            "idusuario": usuario["idusuario"],
            "username": usuario["username"],
            "password": usuario["password"], 
            "email": usuario["email"],
            "telefono": usuario["telefono"],
            "pais": usuario["pais"],
            "edad": usuario["edad"],
            "foto": usuario["foto"] 
        }

        # Enviar la solicitud PUT al backend para actualizar el usuario
        response = requests.put(f"{API_BASE_URL}/auth/update/{usuario['idusuario']}", json=usuarioCompleto)

        if response.status_code == 200:
            session["usuario"] = usuarioCompleto  # Actualizar la sesión con los nuevos datos
            flash("Foto de perfil actualizada correctamente", "success")
        else:
            print("Error:", response.text)
            flash("Error al actualizar la foto de perfil en el servidor", "danger")
    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True)


