from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

API_BASE_URL = "http://localhost:5001"

# Página principal: Login
@app.route("/")
def index():
    # Obtener usuarios desde la API
    response = requests.get(f"{API_BASE_URL}/auth/users")
    usuarios = response.json() if response.status_code == 200 else []
    return render_template("login.html", usuarios=usuarios)

# Página de actividades
@app.route('/actividad.html')
def actividad():
    return render_template('actividad.html')

# Dashboard del usuario
@app.route("/dashboard.html")
def dashboard():
    return render_template("dashboard.html")

<<<<<<< HEAD
# Registro: muestra la vista y procesa el registro
@app.route("/register", methods=["GET", "POST"])
def register():
=======
@app.route("/sobrenosotros.html")
def sobre_nosotros():
    return render_template("sobrenosotros.html")

@app.route("/login", methods=["POST"])
def login():
    # Capturar datos del formulario
    data = {
        "username": request.form["username"],
        "password": request.form["password"]
    }
    # Enviar datos a la API
    response = requests.post(f"{API_BASE_URL}/auth/login", json=data)
    if response.status_code == 200:
        usuario = response.json().get("usuario")  # Extrae los datos del usuario
        return redirect(url_for("dashboard", username=usuario["username"]))
    elif response.status_code == 401:
        return "Error: Usuario o contraseña incorrectos", 401
    else:
        return f"Error en la conexión con la API: {response.text}", response.status_code


@app.route("/registro", methods=["GET", "POST"])
def registro():
>>>>>>> 30d6e6c43f66ff5ee8b690d1e5b663ee94965d14
    if request.method == "POST":
        # Enviar datos del formulario a la API
        data = {
            "username": request.form["username"],
            "password": request.form["password"]
        }
        response = requests.post(f"{API_BASE_URL}/auth/registro", json=data)
        if response.status_code == 200:
<<<<<<< HEAD
            return redirect(url_for("index"))  # Redirige al login después del registro
        else:
            return f"Error al registrar: {response.text}", response.status_code
    return render_template("register.html")
=======
            return redirect(url_for("login.html"))
    return render_template("registro.html")
>>>>>>> 30d6e6c43f66ff5ee8b690d1e5b663ee94965d14

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
        return redirect(url_for("dashboard", username=usuario["username"]))
    elif response.status_code == 401:
        return "Error: Usuario o contraseña incorrectos", 401
    else:
        return f"Error en la conexión con la API: {response.text}", response.status_code

if __name__ == "__main__":
    app.run(debug=True)
