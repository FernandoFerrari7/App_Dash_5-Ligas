from flask import Flask, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State

# Inicializar la aplicación Flask
server = Flask(__name__)
server.secret_key = 'mi_secreto'

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'login'

# Definir usuario
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Diccionario de usuarios
users = {"admin": {"password": "admin"}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Layout del login en forma de modal (popup)
login_modal = dbc.Modal([
    dbc.ModalHeader("Iniciar Sesión"),
    dbc.ModalBody([
        dcc.Input(id="username", type="text", placeholder="Usuario", className="form-control"),
        dcc.Input(id="password", type="password", placeholder="Contraseña", className="form-control", style={"margin-top": "10px"}),
        html.Button("Ingresar", id="login-button", n_clicks=0, className="btn btn-primary", style={"margin-top": "10px"}),
        html.Div(id="login-output", style={"margin-top": "10px", "text-align": "center", "color": "red"}),
    ]),
], id="login-modal", is_open=False)

# Callback para manejar el login y abrir/cerrar el modal
login_callbacks = [
    Output("login-output", "children"),
    Output("login-modal", "is_open"),
    Input("login-button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    State("login-modal", "is_open"),
]

def login(n_clicks, username, password, is_open):
    if n_clicks:
        if username in users and users[username]["password"] == password:
            user = User(username)
            login_user(user)
            return "Inicio de sesión exitoso", False
        return "Usuario o contraseña incorrectos", True
    return "", is_open







