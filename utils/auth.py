from flask import Flask, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input, State

# Inicializar la aplicación Flask
server = Flask(__name__)
server.secret_key = 'mi_secreto'  # Cambia esto en producción

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)

# Definir clase de usuario
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Diccionario de usuarios (en producción usar base de datos)
users = {"admin": {"password": "admin"}}

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

# Ruta para logout
@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# Layout del login en forma de modal (popup) - MEJORADO
login_modal = dbc.Modal([
    dbc.ModalHeader([
        html.H3("INICIAR SESIÓN", className="modal-title", 
               style={"fontSize": "2.5rem", "letterSpacing": "2px", "textAlign": "center", "width": "100%"})
    ], style={"backgroundColor": "#2c3e50", "borderBottom": "2px solid #3498db"}),
    
    dbc.ModalBody([
        html.Div([
            html.I(className="fas fa-user", style={"fontSize": "80px", "color": "#3498db", "marginBottom": "30px"}),
            
            dbc.Input(
                id="username", 
                type="text", 
                placeholder="Usuario", 
                className="form-control login-input",
                style={
                    "fontSize": "1.3rem", 
                    "padding": "15px", 
                    "borderRadius": "10px",
                    "marginBottom": "25px",
                    "backgroundColor": "#1a2533",
                    "color": "white",
                    "border": "1px solid #3e5771"
                }
            ),
            
            dbc.Input(
                id="password", 
                type="password", 
                placeholder="Contraseña", 
                className="form-control login-input",
                style={
                    "fontSize": "1.3rem", 
                    "padding": "15px", 
                    "borderRadius": "10px",
                    "marginBottom": "25px",
                    "backgroundColor": "#1a2533",
                    "color": "white",
                    "border": "1px solid #3e5771"
                }
            ),
            
            dbc.Button(
                "INGRESAR", 
                id="login-button", 
                n_clicks=0, 
                className="btn btn-primary login-button",
                style={
                    "fontSize": "1.5rem", 
                    "fontWeight": "bold", 
                    "padding": "15px", 
                    "width": "100%",
                    "borderRadius": "10px",
                    "backgroundColor": "#3498db",
                    "border": "none",
                    "boxShadow": "0 5px 15px rgba(0, 0, 0, 0.3)",
                    "letterSpacing": "1px"
                }
            ),
            
            html.Div(
                id="login-output", 
                style={
                    "marginTop": "20px", 
                    "textAlign": "center", 
                    "color": "#ff5252",
                    "fontSize": "1.2rem",
                    "fontWeight": "bold"
                }
            ),
        ], style={"display": "flex", "flexDirection": "column", "alignItems": "center", "padding": "20px"}),
    ], style={"backgroundColor": "#2c3e50", "padding": "30px"}),
], id="login-modal", is_open=False, size="lg", backdrop="static", style={"maxWidth": "500px"})

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
    if n_clicks and username and password:
        if username in users and users[username]["password"] == password:
            user = User(username)
            login_user(user)
            return "Inicio de sesión exitoso", False
        return "Usuario o contraseña incorrectos", True
    return "", is_open

# Función para verificar autenticación
def is_authenticated():
    return current_user.is_authenticated







