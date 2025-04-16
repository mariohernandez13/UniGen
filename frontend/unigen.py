from flask import Flask, render_template, request, redirect, session, url_for, jsonify, flash
import requests

app = Flask(__name__)

# añade una clave secreta para la sesión
app.secret_key = "miclavesecreta123"

API_BASE_URL = "http://localhost:5001"

# Página principal: Login
@app.route("/")
def index():
    # Obtener usuarios desde la API
    response = requests.get(f"{API_BASE_URL}/auth/users")
    usuarios = response.json() if response.status_code == 200 else []
    return render_template("login.html")


@app.route('/inicio')
def inicio():
    usuario = session.get("usuario")
    return render_template('inicio.html', usuario=usuario)


@app.route("/RecuperarContraseña")
def recuperar_contraseña():
    return render_template("RecuperarConstraseña.html")


# Página de actividades
@app.route('/actividad')
def actividad():
    # Llamar al endpoint de la API para obtener todas las actividades
    response = requests.get(f"{API_BASE_URL}/activity/all")
    actividades = response.json() if response.status_code == 200 else []
    return render_template("actividad.html", actividades=actividades)


# Dashboard del usuario
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/sobrenosotros")
def sobre_nosotros():
    usuario = session.get("usuario")
    return render_template("sobrenosotros.html", usuario=usuario)


@app.route("/tienda")
def tienda():
    return render_template("tienda.html")


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
            "username": usuario["username"],
            "email": usuario.get("email"),
            "telefono": usuario.get("telefono"),
            "pais": usuario.get("pais"),
            "edad": usuario.get("edad")
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
            "edad": int(edad)
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

if __name__ == "__main__":
    app.run(debug=True)



