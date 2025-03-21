import dash_bootstrap_components as dbc
from dash import html

# Barra de navegación lateral (sidebar)
sidebar = html.Div(
    [
        html.H2("Menú", className="sidebar-title"),
        html.Hr(),

        dbc.Nav(
            [
                dbc.NavLink("🏠 Home", href="/", active="exact", className="nav-link-home"),
                dbc.NavLink("📊 Dashboard Performance", href="/dashboard-performance", active="exact", className="nav-link"),
                dbc.NavLink("🏥 Dashboard Medicina Deportiva", href="/dashboard-medicina", active="exact", className="nav-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)



