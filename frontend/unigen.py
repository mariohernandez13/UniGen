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
    usuario = session.get("usuario")
    if not usuario:
        flash("Debes iniciar sesión para ver las actividades.", "danger")
        return redirect(url_for("index"))

    usuario_id = usuario["idusuario"]

    # Obtener todas las actividades
    response = requests.get(f"{API_BASE_URL}/activity/all")
    actividades = response.json() if response.status_code == 200 else []

    # Obtener IDs de actividades a las que estoy apuntado
    response_inscripciones = requests.get(f"{API_BASE_URL}/activity/user/{usuario_id}/subscriptions")
    inscripciones = response_inscripciones.json() if response_inscripciones.status_code == 200 else []

    # Obtener actividades creadas por el usuario (usando campo 'creador')
    actividades_creadas = [a for a in actividades if str(a.get("creador")) == str(usuario_id)]

    # Actividades disponibles (no creadas ni inscritas)
    ids_creadas = {a["idactividad"] for a in actividades_creadas}
    ids_inscrito = set(inscripciones)
    actividades_disponibles = [
        a for a in actividades
        if a["idactividad"] not in ids_creadas and a["idactividad"] not in ids_inscrito
    ]

    # Actividades a las que estoy apuntado (detalles)
    actividades_apuntado = [a for a in actividades if a["idactividad"] in ids_inscrito]

    # Añadir participantes y contador a todas las actividades mostradas
    for lista in [actividades_disponibles, actividades_creadas, actividades_apuntado]:
        for actividad in lista:
            participantes_response = requests.get(f"{API_BASE_URL}/activity/{actividad['idactividad']}/participantes")
            participantes = participantes_response.json() if participantes_response.status_code == 200 else []
            actividad["num_participantes"] = len(participantes)
            actividad["participantes"] = [p["nombre"] for p in participantes]

    # Filtros GET para actividades disponibles
    tipo = request.args.get("tipo")
    fecha = request.args.get("fecha")
    lugar = request.args.get("lugar")
    if tipo:
        actividades_disponibles = [a for a in actividades_disponibles if a["tipo"] == tipo]
    if fecha:
        actividades_disponibles = [a for a in actividades_disponibles if a["fecha"] == fecha]
    if lugar:
        actividades_disponibles = [a for a in actividades_disponibles if lugar.lower() in a["lugar"].lower()]

    return render_template(
        "dashboard.html",
        actividades_disponibles=actividades_disponibles,
        actividades_creadas=actividades_creadas,
        actividades_apuntado=actividades_apuntado,
        usuario=usuario
    )

# Endpoint para inscribirse en una actividad
@app.route("/inscribirse/<int:actividad_id>", methods=["POST"])
def inscribirse(actividad_id):
    usuario_id = session.get("usuario", {}).get("idusuario")
    if not usuario_id:
        flash("Debes iniciar sesión para inscribirte en una actividad.", "danger")
        return redirect(url_for("index"))

    response = requests.post(
        f"{API_BASE_URL}/activity/{actividad_id}/subscribe",
        json=usuario_id
    )

    if response.status_code == 200:
        flash("¡Inscripción exitosa!", "success")
    else:
        error_message = response.json().get("message", "Error al inscribirse")
        flash(error_message, "danger")

    return redirect(url_for("dashboard"))

# Endpoint para desinscribirse de una actividad
@app.route("/desinscribirse/<int:actividad_id>", methods=["POST"])
def desinscribirse(actividad_id):
    usuario_id = session.get("usuario", {}).get("idusuario")
    if not usuario_id:
        flash("Debes iniciar sesión para borrarte de una actividad.", "danger")
        return redirect(url_for("index"))

    try:
        response = requests.delete(
            f"{API_BASE_URL}/activity/{actividad_id}/unsubscribe",
            json=usuario_id
        )
        if response.status_code == 200:
            flash(response.json().get("message", "¡Te has borrado de la actividad con éxito!"), "success")
        else:
            error_message = response.json().get("message", "Error al borrarse de la actividad")
            flash(error_message, "danger")
    except Exception as e:
        flash("Error al conectar con la API.", "danger")

    return redirect(url_for("dashboard"))

# Endpoint para crear una actividad
@app.route("/crear_actividad", methods=["POST"])
def crear_actividad():
    usuario = session.get("usuario")
    if not usuario:
        flash("Debes iniciar sesión para crear actividades.", "danger")
        return redirect(url_for("index"))

    # Extraer el ID del usuario desde la sesión
    usuario_id = usuario.get("idusuario")
    if not usuario_id:
        flash("Error al obtener el ID del usuario.", "danger")
        return redirect(url_for("dashboard"))

    # Construir el payload para la actividad
    data = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion"),
        "tipo": request.form.get("tipo"),
        "fecha": request.form.get("fecha"),
        "hora": request.form.get("hora"),
        "lugar": request.form.get("lugar"),
        "duracion": request.form.get("duracion"),
        "creadorId": usuario_id  # Incluye el ID del usuario como creador
    }

    # Enviar la solicitud al backend
    response = requests.post(f"{API_BASE_URL}/activity/create", json=data)

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


