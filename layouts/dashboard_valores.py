from dash import html
from components.navbar import sidebar  # Importamos la barra lateral

# Definir el layout del Dashboard Valores de Mercado
layout = html.Div([
    html.Div([
        sidebar,  # Barra de navegación lateral
        html.Div([
            html.H1("Dashboard de Valores de Mercado"),
            html.P("Aquí irán los datos y gráficos sobre valores de mercado.")
        ], className="dashboard-content")  # Mantiene el espaciado correcto
    ], className="dashboard-container")
])



