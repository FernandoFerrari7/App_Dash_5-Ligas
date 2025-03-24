import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# Importar el servidor Flask y las funciones de autenticación
from utils.auth import server, login_modal, login_callbacks, login, is_authenticated

# Importar layouts
from layouts.home import layout as home_layout
from layouts.dashboard_performance import layout as dashboard_performance_layout
from layouts.dashboard_medicina import layout as dashboard_medicina_layout

# Configurar la aplicación Dash con Flask server existente
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[
        dbc.themes.DARKLY,
    ],
    suppress_callback_exceptions=True
)

# Layout principal con rutas y autenticación
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    login_modal,  # Modal de login
    html.Div(id='logout-container', className='logout-btn'),  # Botón de logout
    html.Div(id='page-content')  # Contenido de página
])

# Navegación protegida por autenticación
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/dashboard-performance':
        if not is_authenticated():
            return html.Div([
                html.H3("Necesitas iniciar sesión para acceder a esta página", className="text-center text-danger"),
                dcc.Location(id='redirect-home', pathname='/', refresh=True)
            ])
        return dashboard_performance_layout
    elif pathname == '/dashboard-medicina':
        if not is_authenticated():
            return html.Div([
                html.H3("Necesitas iniciar sesión para acceder a esta página", className="text-center text-danger"),
                dcc.Location(id='redirect-home', pathname='/', refresh=True)
            ])
        return dashboard_medicina_layout
    else:
        return home_layout

# Mostrar/ocultar botón de logout
@app.callback(
    Output('logout-container', 'children'),
    Input('url', 'pathname')
)
def update_logout_button(pathname):
    if is_authenticated():
        return html.A('Cerrar Sesión', href='/logout', className='logout-btn')
    return ''

# Abrir modal de login si se accede a ruta protegida sin login
@app.callback(
    Output('login-modal', 'is_open', allow_duplicate=True),
    Input('url', 'pathname'),
    State('login-modal', 'is_open'),
    prevent_initial_call=True
)
def open_login_modal(pathname, is_open):
    if (pathname == '/dashboard-performance' or pathname == '/dashboard-medicina') and not is_authenticated():
        return True
    return is_open

# Abrir modal desde botón en home
@app.callback(
    Output('login-modal', 'is_open', allow_duplicate=True),
    Input('open-login-button', 'n_clicks'),
    State('login-modal', 'is_open'),
    prevent_initial_call=True
)
def open_login_from_button(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Callback de autenticación
@app.callback(*login_callbacks)
def handle_login(n_clicks, username, password, is_open):
    return login(n_clicks, username, password, is_open)

# Importar callbacks después de definir app
from callbacks.performance_callbacks import *
from callbacks.medicina_callbacks import *
from callbacks.pdf_export import *

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)


























