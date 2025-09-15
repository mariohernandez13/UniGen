from flask import Flask, render_template, request, redirect, session, url_for, jsonify, flash
import requests
import os
from werkzeug.utils import secure_filename
from flask import render_template_string
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import google.oauth2.credentials

CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "client_secret_91322234665-mvm37frh56lgntu2b9bnja59fdm5t3op.apps.googleusercontent.com.json")
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask(__name__)

# añade una clave secreta para la sesión
app.secret_key = "miclavesecreta123"

@app.route("/authorize")
def authorize():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for("oauth2callback", _external=True),
    )
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/oauth2callback")
def oauth2callback():
    state = session["state"]
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for("oauth2callback", _external=True),
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)
    return redirect(url_for("dashboard"))

@app.route("/calendar")
def calendar():
    if "credentials" not in session:
        return redirect(url_for("authorize"))
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])
    service = build("calendar", "v3", credentials=credentials)

    # Obtén todos los calendarios del usuario
    calendar_list = service.calendarList().list().execute()
    eventos = []

    for cal in calendar_list.get('items', []):
        cal_id = cal['id']
        # Solo muestra eventos futuros
        events_result = service.events().list(
            calendarId=cal_id,
            maxResults=200,
            singleEvents=True,
            orderBy='startTime',
            timeMin=datetime.utcnow().isoformat() + 'Z'
        ).execute()
        for ev in events_result.get('items', []):
            # Añade el nombre del calendario como fuente
            ev['calendarName'] = cal.get('summary', '')
            eventos.append(ev)

    return jsonify(eventos)

@app.route("/calendar/status")
def calendar_status():
    return jsonify({"authenticated": "credentials" in session})

def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }

API_BASE_URL = "http://localhost:5001"
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "IMAGES", "perfiles")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "svg", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ARTICULOS_VALOR = {
    "crown.png": 10000,
    "graduate-hat.png": 5350,
    "cap.png": 4200,
    "party-hat.png": 3250,
    "chef.png": 2500,
    "wizard-hat.png": 1180,
    "medal.png": 920,
    "military-rank (1).png": 500,
    "military-rank.png": 300,
    "military-rank (2).png": 280,
    # Añade más si tienes
}
@app.route("/api/actividades_apuntado")
def api_actividades_apuntado():
    usuario = session.get("usuario")
    if not usuario:
        return jsonify([])

    usuario_id = usuario["idusuario"]

    # Obtener todas las actividades
    response = requests.get(f"{API_BASE_URL}/activity/all")
    actividades = response.json() if response.status_code == 200 else []

    # Obtener IDs de actividades a las que estoy apuntado
    response_inscripciones = requests.get(f"{API_BASE_URL}/activity/user/{usuario_id}/subscriptions")
    inscripciones = response_inscripciones.json() if response_inscripciones.status_code == 200 else []

    # Si inscripciones es una lista de objetos, extrae los IDs
    if inscripciones and isinstance(inscripciones[0], dict) and "idactividad" in inscripciones[0]:
        inscripciones = [i["idactividad"] for i in inscripciones]

    print("Inscripciones:", inscripciones)
    print("Actividades:", actividades)

    # Actividades a las que estoy apuntado (detalles)
    actividades_apuntado = [a for a in actividades if str(a["idactividad"]) in [str(i) for i in inscripciones]]
    print("Actividades apuntado:", actividades_apuntado)  # Para depuración

    return jsonify(actividades_apuntado)
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

    # Obtener artículos comprados
    response = requests.get(f"{API_BASE_URL}/auth/usuario/{usuario['idusuario']}/articulos")
    articulos = response.json() if response.status_code == 200 else []

    # Definir listas de nombres para gorros y chapas
    GORROS = {
        "crown.png", "graduate-hat.png", "cap.png", "party-hat.png", "chef.png", "wizard-hat.png"
    }
    CHAPAS = {
        "medal.png", "military-rank.png", "military-rank (1).png", "military-rank (2).png"
    }

    # Buscar el gorro más valioso
    gorro_mas_valioso = None
    max_valor_gorro = -1
    # Buscar la chapa más valiosa
    chapa_mas_valiosa = None
    max_valor_chapa = -1

    for articulo in articulos:
        nombre = articulo.get("articulo", "")
        valor = ARTICULOS_VALOR.get(nombre, 0)
        if nombre in GORROS and valor > max_valor_gorro:
            max_valor_gorro = valor
            gorro_mas_valioso = articulo
        if nombre in CHAPAS and valor > max_valor_chapa:
            max_valor_chapa = valor
            chapa_mas_valiosa = articulo

    return render_template(
        "modalUsuario.html",
        usuario=usuario,
        gorro_mas_valioso=gorro_mas_valioso,
        chapa_mas_valiosa=chapa_mas_valiosa
    )

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
            # Añade los artículos a cada participante
            for participante in participantes:
                response_articulos = requests.get(f"{API_BASE_URL}/auth/usuario/{participante['idusuario']}/articulos")
                participante['articulos'] = response_articulos.json() if response_articulos.status_code == 200 else []
            actividad["num_participantes"] = len(participantes)
            actividad["participantes"] = participantes  # <-- Aquí guardas el objeto completo

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

    # Establecer la pestaña activa por defecto como "crear"
    active_tab = request.args.get("active_tab", "crear")

    # Pasar la lista de IDs de actividades inscritas al contexto
    ids_inscrito = list(ids_inscrito)

    return render_template(
        "dashboard.html",
        actividades_disponibles=actividades_disponibles,
        actividades_creadas=actividades_creadas,
        actividades_apuntado=actividades_apuntado,
        usuario=usuario,
        active_tab=active_tab,
        ids_inscrito=ids_inscrito
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

    # Redirige a la página del dashboard con la pestaña "creadas" activa
    return redirect(url_for("dashboard", active_tab="creadas"))

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

    # Redirige a la página del dashboard with la pestaña "apuntado" activa
    return redirect(url_for("dashboard", active_tab="apuntado"))

# Endpoint para crear una actividad
@app.route("/crear_actividad", methods=["POST"])
def crear_actividad():
    usuario = session.get("usuario")
    if not usuario:
        flash("Debes iniciar sesión para crear actividades.", "danger")
        return redirect(url_for("index"))

    usuario_id = usuario.get("idusuario")
    if not usuario_id:
        flash("Error al obtener el ID del usuario.", "danger")
        return redirect(url_for("dashboard"))

    # Obtén la duración en minutos
    duracion = int(request.form.get("duracion", 0))
    # Calcula los puntos: 50 puntos por cada 60 minutos
    puntos = max(50, (duracion // 60) * 50)
    if duracion % 60 != 0:
        puntos += 50  # Si hay minutos extra, suma otros 50 puntos

    data = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion"),
        "tipo": request.form.get("tipo"),
        "fecha": request.form.get("fecha"),
        "hora": request.form.get("hora"),
        "lugar": request.form.get("lugar"),
        "duracion": duracion,
        "creadorId": usuario_id,
        "puntos": puntos  # Añade los puntos calculados
    }

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
    descuento_activo = False
    bonus_activo = False
    if usuario and usuario.get("descuento_hasta"):
        try:
            descuento_activo = datetime.fromisoformat(usuario["descuento_hasta"]) > datetime.now()
        except Exception:
            descuento_activo = False
    if usuario and usuario.get("bonus_creditos_hasta"):
        try:
            bonus_activo = datetime.fromisoformat(usuario["bonus_creditos_hasta"]) > datetime.now()
        except Exception:
            bonus_activo = False
    return render_template("tienda.html", usuario=usuario, descuento_activo=descuento_activo, bonus_activo=bonus_activo)


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
        
        # Guardar todo en la sesión, incluyendo puntos
        session["usuario"] = {
            "idusuario": usuario["idusuario"],
            "username": usuario["username"],
            "password": data["password"],
            "email": usuario.get("email"),
            "telefono": usuario.get("telefono"),
            "pais": usuario.get("pais"),
            "edad": usuario.get("edad"),
            "foto": usuario.get("foto", "default-avatar.svg"),
            "puntos": usuario.get("puntos", 0), 
            "papeletas": usuario.get("papeletas", 0),  
           "descuento_hasta": usuario.get("descuento_hasta", "")
        }
        
        return redirect(url_for("inicio"))
    elif response.status_code == 401:
        flash("Usuario o contraseña incorrectos", "danger")
        return render_template("login.html")
    else:
        return f"Error en la conexión con la API: {response.text}", response.status_code
    
@app.route("/borrar_actividad/<int:actividad_id>", methods=["POST"])
def borrar_actividad(actividad_id):
    usuario = session.get("usuario")
    if not usuario:
        flash("Debes iniciar sesión para borrar actividades.", "danger")
        return redirect(url_for("index"))

    response = requests.delete(f"{API_BASE_URL}/activity/delete/{actividad_id}")
    if response.status_code == 200:
        flash("Actividad borrada correctamente.", "success")
    else:
        flash(response.json().get("message", "Error al borrar la actividad"), "danger")
    
    # Redirige a la página del dashboard with la pestaña "disponibles" activa
    return redirect(url_for("dashboard", active_tab="creadas"))

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
        return redirect(url_for("modal_usuario"))

    file = request.files["foto"]
    if file.filename == "":
        flash("Nombre de archivo vacio", "danger")
        return redirect(url_for("modal_usuario"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        usuario = session.get("usuario")
        usuario["foto"] = filename

        # Envía todos los datos, incluida la nueva foto
        data = {
            "username": usuario["username"],
            "email": usuario["email"],
            "telefono": usuario.get("telefono", ""),
            "ciudad": usuario.get("ciudad", ""),
            "estudios": usuario.get("estudios", ""),
            "foto": filename
        }
        response = requests.put(f"{API_BASE_URL}/auth/usuario/{usuario['idusuario']}/editar_perfil", json=data)

        if response.status_code == 200:
            usuario.update(data)
            session["usuario"] = usuario
            flash("Foto de perfil actualizada correctamente", "success")
        else:
            flash("Error al actualizar la foto de perfil en el servidor", "danger")
    return redirect(url_for("modal_usuario"))

@app.route("/filtrar_actividades_disponibles")
def filtrar_actividades_disponibles():
    usuario = session.get("usuario")
    if not usuario:
        return "", 401

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

    # Filtros GET para actividades disponibles (corrige formato y mayúsculas)
    tipo = request.args.get("tipo")
    fecha = request.args.get("fecha")
    lugar = request.args.get("lugar")
    if tipo:
        actividades_disponibles = [a for a in actividades_disponibles if a["tipo"].lower() == tipo.lower()]
    if fecha:
        actividades_disponibles = [a for a in actividades_disponibles if a["fecha"].startswith(fecha)]
    if lugar:
        actividades_disponibles = [a for a in actividades_disponibles if lugar.lower() in a["lugar"].lower()]

    # Añadir participantes y contador a las actividades filtradas
    for actividad in actividades_disponibles:
        participantes_response = requests.get(f"{API_BASE_URL}/activity/{actividad['idactividad']}/participantes")
        participantes = participantes_response.json() if participantes_response.status_code == 200 else []
        actividad["num_participantes"] = len(participantes)
        actividad["participantes"] = participantes

    # Renderiza SOLO el bloque de actividades en el MISMO formato que dashboard.html espera
    bloque_html = """
    <div class="row row-cols-1 row-cols-md-2 g-5 justify-content-center">
    {% for actividad in actividades_disponibles %}
        <div class="col">
            <div class="card actividad-card shadow-lg w-100 text-white position-relative overflow-hidden p-0" style="min-height: 260px;">
                <div class="actividad-bg" style="background-image: url('{{ url_for('static', filename='IMAGES/' + actividad.foto) }}');"></div>
                <div class="actividad-overlay d-flex flex-column justify-content-center align-items-start h-100 p-5">
                    <h2 class="fw-bold mb-3" style="font-size: 2.7rem; letter-spacing: 1px; text-shadow: 0 2px 12px #0008;">{{ actividad.nombre }}</h2>
                    <button class="btn btn-lg btn-primary ver-mas-btn px-5 py-3 mt-2"
                        data-bs-toggle="modal"
                        data-bs-target="#modalActividad{{ actividad.idactividad }}"
                        style="font-size: 1.6rem; border-radius: 2rem; font-weight: 700; box-shadow: 0 2px 12px rgba(59,91,219,0.18);">
                        Ver más
                    </button>
                </div>
            </div>
        </div>
        <!-- Modal Detalle Actividad -->
        <div class="modal fade" id="modalActividad{{ actividad.idactividad }}" tabindex="-1"
            aria-labelledby="modalActividadLabel{{ actividad.idactividad }}" aria-hidden="true">
            <div class="modal-dialog modal-xl modal-dialog-centered">
                <div class="modal-content rounded-4">
                    <div class="modal-header" style="background: #f8fafc;">
                        <h2 class="modal-title fw-bold w-100 text-center"
                            id="modalActividadLabel{{ actividad.idactividad }}"
                            style="font-size: 2.8rem; color: #3b5bdb; letter-spacing: 1px;">
                            {{ actividad.nombre }}
                        </h2>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                            aria-label="Cerrar"></button>
                    </div>
                    <div class="modal-body px-5 py-4">
                        <div class="mb-4 text-center">
                            <span class="badge bg-primary fs-4 px-4 py-2 mb-3"
                                style="font-size: 1.5rem;">{{ actividad.tipo }}</span>
                        </div>
                        <ul class="list-unstyled mb-4" style="font-size: 2rem;">
                            <li class="mb-3"><strong>📍 Lugar:</strong> <span
                                    style="color:#3b5bdb;">{{ actividad.lugar }}</span></li>
                            <li class="mb-3">
                                <strong>🗓️ Fecha:</strong>
                                <span style="color:#3b5bdb;">
                                    {% set fecha = actividad.fecha.split(' ')[0] if ' ' in actividad.fecha else actividad.fecha.split('T')[0] %}
                                    {% set partes = fecha.split('-') %}
                                    {{ partes[2] }}/{{ partes[1] }}/{{ partes[0] }}
                                </span>
                            </li>
                            <li class="mb-3"><strong>🕒 Hora:</strong> <span
                                    style="color:#3b5bdb;">{{ actividad.hora }}</span></li>
                            <li class="mb-3"><strong>⏳ Duración:</strong> <span
                                    style="color:#3b5bdb;">{{ actividad.duracion }} min</span></li>
                        </ul>
                        <div class="mb-4">
                            <h4 class="fw-bold text-secondary" style="font-size: 2.2rem;">
                                Descripción</h4>
                            <p style="font-size: 1.7rem;">{{ actividad.descripcion }}</p>
                        </div>
                        <div class="mb-4">
                            <h5 class="fw-bold mb-2" style="font-size: 2rem;">
                                Participantes inscritos: {{ actividad.num_participantes }}
                            </h5>
                            {% if actividad.num_participantes > 0 %}
                            <ul class="list-group list-group-flush mb-4" style="font-size: 1.5rem;">
                                {% for participante in actividad.participantes %}
                                <li class="list-group-item d-flex align-items-center justify-content-between">
                                    <span class="flex-grow-1">{{ participante.usuario.username }}</span>
                                    <button type="button"
                                        class="btn btn-outline-info btn-sm ms-2"
                                        data-bs-toggle="modal"
                                        data-bs-target="#modalPerfilUsuario{{ participante.idusuario }}"
                                        title="Ver perfil"> Ver Perfil
                                        <i class="bi bi-person-circle"></i>
                                    </button>
                                </li>
                                {% endfor %}
                            </ul>
                            {% else %}
                            <p class="text-muted" style="font-size: 1.3rem;">No hay participantes aún.</p>
                            {% endif %}
                        </div>
                        <form action="{{ url_for('inscribirse', actividad_id=actividad.idactividad) }}" method="POST"
                            class="mt-4">
                            <button type="submit" class="btn btn-success btn-lg w-100"
                                style="font-size: 1.5rem; border-radius: 1.5rem;">
                                Apuntarme
                            </button>
                        </form>
                    </div>
                    <div class="modal-footer" style="background: #f8fafc;">
                        <button type="button" class="btn btn-secondary btn-lg" data-bs-dismiss="modal"
                            style="font-size: 1.2rem;">Cerrar</button>
                    </div>
                </div>
            </div>
        </div>
        <!-- Fin Modal -->
    {% endfor %}
    {% if actividades_disponibles|length == 0 %}
        <div class="col-12 text-center text-muted">No hay actividades disponibles.</div>
    {% endif %}
    </div>
    """

    return render_template_string(bloque_html, actividades_disponibles=actividades_disponibles)

@app.route("/editar_perfil", methods=["POST"])
def editar_perfil():
    usuario = session.get("usuario")
    if not usuario:
        flash("Debes iniciar sesión.", "danger")
        return redirect(url_for("modal_usuario"))

    usuario_id = usuario["idusuario"]
    data = {
        "username": request.form.get("username", ""),
        "email": request.form.get("email", ""),
        "telefono": request.form.get("telefono", ""),
        "foto": usuario.get("foto", "default-avatar.svg")
    }
    response = requests.put(f"{API_BASE_URL}/auth/usuario/{usuario_id}/editar_perfil", json=data)
    print("STATUS:", response.status_code)
    print("RESPUESTA:", response.text)
    if response.status_code == 200:
        # Refresca los datos del usuario desde la API
        user_response = requests.get(f"{API_BASE_URL}/auth/users")
        if user_response.status_code == 200:
            usuarios = user_response.json()
            usuario_actualizado = next((u for u in usuarios if u["idusuario"] == usuario_id), None)
            if usuario_actualizado:
                session["usuario"] = usuario_actualizado
        flash("Perfil actualizado correctamente.", "success")
    else:
        flash("No se pudo actualizar el perfil. " + response.text, "danger")
    return redirect(url_for("modal_usuario"))

@app.route("/validar_creditos", methods=["POST"])
def validar_creditos():
    data = request.json
    idusuario = data.get("idusuario")
    idactividad = data.get("idactividad")
    puntos = data.get("puntos")
    if idusuario is None or idactividad is None or puntos is None:
        return jsonify({"success": False, "message": "Datos incompletos"}), 400

    usuario = session.get("usuario")
    bonus_activo = False
    if usuario and usuario.get("bonus_creditos_hasta"):
        try:
            # Soporta formato ISO y con espacio
            bonus_activo = (
                datetime.fromisoformat(usuario["bonus_creditos_hasta"].replace(" ", "T"))
                > datetime.now()
            )
        except Exception:
            pass

    # DUPLICA los puntos si el bonus está activo
    if bonus_activo:
        puntos = puntos * 2

    # Obtener la lista de participantes de la actividad
    response = requests.get(f"{API_BASE_URL}/activity/{idactividad}/participantes")
    participantes = response.json() if response.status_code == 200 else []

    # Verifica que el usuario no tenga creditos_validados en True
    participante = next((p for p in participantes if str(p.get("idusuario")) == str(idusuario)), None)
    if participante and participante.get("creditos_validados") is True:
        return jsonify({"success": False, "message": "Créditos ya validados para este usuario"}), 400
    
    response = requests.post(
        f"{API_BASE_URL}/auth/sumar_creditos",
        json={"idusuario": int(idusuario), "idactividad": int(idactividad), "puntos": int(puntos)}
    )
    if response.status_code == 200:
        # Actualiza los puntos en la sesión
        nuevos_puntos = response.json().get("puntos")
        usuario = session.get("usuario")
        if usuario and nuevos_puntos is not None:
            usuario["puntos"] = nuevos_puntos
            session["usuario"] = usuario
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Error al validar créditos"}), 500

from flask import jsonify

@app.route("/comprar_articulo", methods=["POST"])
def comprar_articulo():
    usuario = session.get("usuario")
    if not usuario:
        return jsonify({"success": False, "message": "Debes iniciar sesión para comprar."}), 401

    data = request.json
    coste = int(data.get("coste", 0))
    nombre = data.get("nombre", "artículo")
    imagen = data.get("imagen", "")

    puntos_actuales = int(usuario.get("puntos", 0))

    if puntos_actuales < coste:
        return jsonify({"success": False, "message": "No tienes suficientes créditos para comprar este artículo."})

    # Resta los puntos y actualiza en la sesión
    nuevos_puntos = puntos_actuales - coste
    usuario["puntos"] = nuevos_puntos

    # --- NUEVO: Sumar papeleta si es sorteo ---
    if "sorteo mensual" in nombre.lower() or "raffle" in nombre.lower():
        usuario["papeletas"] = usuario.get("papeletas", 0) + 1
    session["usuario"] = usuario

    # Actualiza los puntos y papeletas en la base de datos
    response = requests.put(
        f"{API_BASE_URL}/auth/update/{usuario['idusuario']}",
        json={
            "username": usuario["username"],
            "email": usuario["email"],
            "password": usuario.get("password", ""),
            "telefono": usuario.get("telefono", ""),
            "pais": usuario.get("pais", ""),
            "edad": usuario.get("edad", 0),
            "foto": usuario.get("foto", "default-avatar.svg"),
            "puntos": nuevos_puntos,
            "papeletas": usuario.get("papeletas", 0)  # <-- Añade esto
        }
    )
    if response.status_code != 200:
        return jsonify({"success": False, "message": "No se pudo actualizar los puntos en la base de datos."}), 500

    # Guarda el artículo comprado en la base de datos
    response_articulo = requests.post(
        f"{API_BASE_URL}/auth/usuario/{usuario['idusuario']}/comprar_articulo",
        json={"articulo": imagen if imagen else nombre}
    )
    if response_articulo.status_code != 200:
        return jsonify({"success": False, "message": "No se pudo guardar el artículo en el perfil."}), 500

    return jsonify({
        "success": True,
        "message": f"¡Has comprado {nombre} correctamente!",
        "puntos": nuevos_puntos,
        "papeletas": usuario.get("papeletas", 0)  # <-- Devuelve el nuevo número de papeletas
    })

@app.route('/comprar_descuento', methods=['POST'])
def comprar_descuento():
    usuario = session.get("usuario")
    if not usuario:
        return jsonify(success=False, message="Debes iniciar sesión."), 401

    COSTE_DESCUENTO = 250
    puntos_actuales = int(usuario.get("puntos", 0))

    # No dejar comprar si ya tiene descuento activo
    if usuario.get("descuento_hasta"):
        try:
            if datetime.strptime(usuario["descuento_hasta"], "%Y-%m-%d %H:%M:%S") > datetime.now():
                return jsonify(success=False, message="Ya tienes un descuento activo.")
        except Exception:
            pass

    if puntos_actuales < COSTE_DESCUENTO:
        return jsonify(success=False, message="No tienes suficientes créditos.")

    # Resta créditos y actualiza descuento_hasta
    usuario["puntos"] -= COSTE_DESCUENTO
    descuento_hasta = (datetime.now() + timedelta(hours=2)).isoformat()
    usuario["descuento_hasta"] = descuento_hasta

    # Actualiza en la API
    response = requests.put(
        f"{API_BASE_URL}/auth/update/{usuario['idusuario']}",
        json={
            "username": usuario["username"],
            "email": usuario["email"],
            "password": usuario.get("password", ""),
            "telefono": usuario.get("telefono", ""),
            "pais": usuario.get("pais", ""),
            "edad": usuario.get("edad", 0),
            "foto": usuario.get("foto", "default-avatar.svg"),
            "puntos": usuario["puntos"],
            "papeletas": usuario.get("papeletas", 0),
            "descuento_hasta": usuario.get("descuento_hasta", "")
        }
    )
    if response.status_code != 200:
        return jsonify(success=False, message="No se pudo activar el descuento."), 500

    session["usuario"] = usuario
    return jsonify(success=True, descuento_hasta=descuento_hasta, puntos=usuario["puntos"])

@app.route('/comprar_bonus_creditos', methods=['POST'])
def comprar_bonus_creditos():
    usuario = session.get("usuario")
    if not usuario:
        return jsonify(success=False, message="Debes iniciar sesión."), 401

    COSTE_BONUS = 500
    puntos_actuales = int(usuario.get("puntos", 0))

    # No dejar comprar si ya tiene bonus activo
    if usuario.get("bonus_creditos_hasta"):
        try:
            if datetime.strptime(usuario["bonus_creditos_hasta"], "%Y-%m-%d %H:%M:%S") > datetime.now():
                return jsonify(success=False, message="Ya tienes el bonus activo.")
        except Exception:
            pass

    if puntos_actuales < COSTE_BONUS:
        return jsonify(success=False, message="No tienes suficientes créditos.")

    # Resta créditos y actualiza bonus_creditos_hasta
    usuario["puntos"] -= COSTE_BONUS
    bonus_creditos_hasta = (datetime.now() + timedelta(hours=2)).isoformat()
    usuario["bonus_creditos_hasta"] = bonus_creditos_hasta

    # Actualiza en la API
    response = requests.put(
        f"{API_BASE_URL}/auth/update/{usuario['idusuario']}",
        json={
            "username": usuario["username"],
            "email": usuario["email"],
            "password": usuario.get("password", ""),
            "telefono": usuario.get("telefono", ""),
            "pais": usuario.get("pais", ""),
            "edad": usuario.get("edad", 0),
            "foto": usuario.get("foto", "default-avatar.svg"),
            "puntos": usuario["puntos"],
            "papeletas": usuario.get("papeletas", 0),
            "descuento_hasta": usuario.get("descuento_hasta", ""),
            "bonus_creditos_hasta": usuario.get("bonus_creditos_hasta", "")
        }
    )
    if response.status_code != 200:
        return jsonify(success=False, message="No se pudo activar el bonus."), 500

    session["usuario"] = usuario
    return jsonify(success=True, bonus_creditos_hasta=bonus_creditos_hasta, puntos=usuario["puntos"])

@app.route("/editar_actividad/<int:actividad_id>", methods=["POST"])
def editar_actividad(actividad_id):
    usuario = session.get("usuario")
    if not usuario:
        flash("Debes iniciar sesión para editar actividades.", "danger")
        return redirect(url_for("dashboard", active_tab="creadas"))

    data = {
        "nombre": request.form.get("nombre"),
        "descripcion": request.form.get("descripcion"),
        "tipo": request.form.get("tipo"),
        "fecha": request.form.get("fecha"),
        "hora": request.form.get("hora"),
        "lugar": request.form.get("lugar"),
        "duracion": int(request.form.get("duracion", 0))
    }

    response = requests.put(f"{API_BASE_URL}/activity/update/{actividad_id}", json=data)
    if response.status_code == 200:
        flash("¡Actividad editada correctamente!", "success")
    else:
        flash("Error al editar la actividad", "danger")
    return redirect(url_for("dashboard", active_tab="creadas"))

if __name__ == "__main__":
    app.run(debug=True)
