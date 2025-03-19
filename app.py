import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from layouts import home, dashboard_performance, dashboard_valores
import callbacks.performance_callbacks  # Importamos callbacks

# Inicializar la app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Football Dashboard"

# Layout de la app
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# Callback para manejar la navegación
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/dashboard-performance":
        return dashboard_performance.layout
    elif pathname == "/dashboard-valores":
        return dashboard_valores.layout
    else:
        return home.layout  # Home sin sidebar

if __name__ == "__main__":
    app.run_server(debug=True)

























