from dash import html
import dash_bootstrap_components as dbc

# Definir el layout del Home
layout = html.Div([
    # Contenedor de los títulos principales
    html.Div([
        html.H1("STATS", className="title-left"),
        html.H1("SEASON 2024-2025", className="title-right")
    ], className="header-container"),
    
    # Sección de Ligas con Logos
    html.Div([
        html.Div([
            html.Img(src="/assets/Premier League.png", className="league-logo"),
        ], className="league-box"),
        
        html.Div([
            html.Img(src="/assets/La Liga.png", className="league-logo"),
        ], className="league-box"),
        
        html.Div([
            html.Img(src="/assets/Serie A.png", className="league-logo"),
        ], className="league-box"),
        
        html.Div([
            html.Img(src="/assets/Bundesliga.png", className="league-logo"),
        ], className="league-box"),
        
        html.Div([
            html.Img(src="/assets/Ligue 1.png", className="league-logo"),
        ], className="league-box")
    ], className="leagues-container"),

    # Nueva fila de banderas alineadas correctamente
    html.Div([
        html.Img(src="/assets/Inglaterra.png", className="country-flag"),
        html.Img(src="/assets/España.png", className="country-flag"),
        html.Img(src="/assets/Italia.png", className="country-flag"),
        html.Img(src="/assets/Alemania.png", className="country-flag"),
        html.Img(src="/assets/Francia.png", className="country-flag"),
    ], className="flags-container"),

    # Espacio extra para distribuir mejor los elementos
    html.Div(className="spacer"),

    # Botones de Navegación
    html.Div([
        dbc.Button("DASHBOARD PERFORMANCE", href="/dashboard-performance", color="primary", className="nav-button"),
        dbc.Button("DASHBOARD VALORES DE MERCADO", href="/dashboard-valores", color="secondary", className="nav-button")
    ], className="button-container"),
])














