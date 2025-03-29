from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

BACKEND_URL = "http://localhost:7229/api/auth"

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        response = requests.post(
            f"{BACKEND_URL}/login",
            json={"username": username, "password": password},
            timeout=5  # Agrega un tiempo de espera para evitar bloqueos
        )
        response.raise_for_status()  # Lanza una excepción si el código no es 2xx

        if response.status_code == 200:
            return redirect(url_for("dashboard", username=username))
        else:
            return "Error: Usuario o contraseña incorrectos", 401
    except requests.exceptions.RequestException as e:
        # Maneja errores de conexión o tiempo de espera
        return f"Error al conectar con el backend: {e}", 500

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/register")
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)