from dash import html, dcc
import dash_bootstrap_components as dbc
from components.navbar import sidebar
from utils.data_loader import df

# 🔹 Definir métricas ofensivas con nombres corregidos
metricas_ofensivas = {
    "Posesión": "Poss",
    "Goles x90": "Per 90 Minutes_Gls",
    "xG x90": "Per 90 Minutes_xG",
    "Progresiones": "Progression"
}

# 🔹 Opciones de ligas
ligas = [{"label": liga, "value": liga} for liga in sorted(df["league"].unique())]

# 🔹 Layout del Dashboard Performance (SIN CAMBIAR EL TAMAÑO DEL GRÁFICO)
layout = html.Div([
    sidebar,  # Barra lateral

    html.Div([
        html.H1("Dashboard de Performance", className="dashboard-title"),

        # 🔹 Contenedor de filtros
        html.Div([
            html.Div([
                html.Label("Métrica:", className="label"),
                dcc.Dropdown(
                    id="dropdown-metrica",
                    options=[{"label": k, "value": v} for k, v in metricas_ofensivas.items()],
                    placeholder="Selecciona una métrica",
                    className="dropdown"
                )
            ], className="filter-box"),

            html.Div([
                html.Label("Liga:", className="label"),
                dcc.Dropdown(
                    id="dropdown-league",
                    options=ligas,
                    placeholder="Selecciona una liga",
                    className="dropdown"
                )
            ], className="filter-box"),

            html.Div([
                html.Label("Equipo:", className="label"),
                dcc.Dropdown(
                    id="dropdown-team",
                    options=[],
                    placeholder="Selecciona un equipo",
                    className="dropdown"
                )
            ], className="filter-box")
        ], className="filtros-container"),

        # 🔹 Contenedor principal con el tamaño original del gráfico
        html.Div([
            html.Div([
                html.Div(id="output-graph", className="graph-content", style={"height": "100%"})
            ], className="graph-container", style={"height": "auto"}),  # Permitir que crezca dinámicamente
            
            html.Div([
                html.Div(id="output-team-stats", className="team-stats-content")  # 🔹 Información del equipo
            ], className="team-info-container")
        ], className="main-content-container", style={"height": "auto"})
    ], className="dashboard-content")
], className="dashboard-container")
























