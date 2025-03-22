import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Importar layouts
from layouts.home import layout as home_layout
from layouts.dashboard_performance import layout as dashboard_performance_layout
from layouts.dashboard_medicina import layout as dashboard_medicina_layout

# Configurar la aplicación Dash con Bootstrap
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.DARKLY,
    ],
    suppress_callback_exceptions=True
)

# Configurar el layout principal con rutas
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callbacks para la navegación
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/dashboard-performance':
        return dashboard_performance_layout
    elif pathname == '/dashboard-medicina':
        return dashboard_medicina_layout
    else:
        # Por defecto, mostrar la página de home
        return home_layout

# Importar callbacks después de definir la aplicación
from callbacks.performance_callbacks import *
from callbacks.medicina_callbacks import *
from callbacks.pdf_export import *

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)

























