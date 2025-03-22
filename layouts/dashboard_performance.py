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

# 🔹 Layout del Dashboard Performance
layout = html.Div([
    sidebar,  # Barra lateral

    html.Div([
        # Título y botón de exportación en la misma fila
        html.Div([
            html.H1("Dashboard de Performance", className="dashboard-title"),
            html.Div([
                dbc.Button(
                    [html.I(className="fas fa-file-pdf mr-2"), " Exportar a PDF"],
                    id="btn-export-pdf",
                    color="danger",
                    className="export-button",
                ),
                dcc.Download(id="download-pdf")
            ], className="export-button-container")
        ], className="header-with-button"),

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

        # 🔹 Contenedor principal con gráfico y ranking
        html.Div([
            # Contenedor del gráfico
            html.Div([
                html.Div(id="output-graph", className="graph-content")
            ], className="graph-container"),
            
            # Contenedor de info del equipo
            html.Div([
                html.Div(id="output-team-stats", className="team-stats-content")
            ], className="team-info-container")
        ], className="main-content-container")
    ], className="dashboard-content")
], className="dashboard-container")

























