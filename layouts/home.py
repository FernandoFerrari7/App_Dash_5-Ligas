from dash import html, dcc
import dash_bootstrap_components as dbc

# Definir el layout del Home con componentes más grandes y mejor distribución del espacio
layout = html.Div([
    # Contenedor de los títulos principales con títulos más grandes y centrados
    html.Div([
        html.Div([
            html.H1("STATS", className="main-title", style={"fontSize": "5rem", "fontWeight": "bold"}),
        ], style={"textAlign": "center", "width": "100%"}),
        
        html.Div([
            html.H1("SEASON 2024-2025", className="main-title", style={"fontSize": "4rem", "fontWeight": "bold"}),
        ], style={"textAlign": "center", "width": "100%"}),
    ], className="header-container", style={"marginBottom": "50px", "marginTop": "30px", "display": "flex", "flexDirection": "column", "alignItems": "center"}),
    
    # Sección de Ligas con Logos mucho más grandes
    html.Div([
        html.Div([
            html.Img(src="/assets/Premier League.png", className="league-logo-large", 
                    style={"width": "200px", "height": "auto"})
        ], className="league-box-large"),
        
        html.Div([
            html.Img(src="/assets/La Liga.png", className="league-logo-large", 
                    style={"width": "200px", "height": "auto"})
        ], className="league-box-large"),
        
        html.Div([
            html.Img(src="/assets/Serie A.png", className="league-logo-large", 
                    style={"width": "200px", "height": "auto"})
        ], className="league-box-large"),
        
        html.Div([
            html.Img(src="/assets/Bundesliga.png", className="league-logo-large", 
                    style={"width": "200px", "height": "auto"})
        ], className="league-box-large"),
        
        html.Div([
            html.Img(src="/assets/Ligue 1.png", className="league-logo-large", 
                    style={"width": "200px", "height": "auto"})
        ], className="league-box-large")
    ], className="leagues-container", style={"marginBottom": "40px"}),

    # Banderas mucho más grandes
    html.Div([
        html.Img(src="/assets/Inglaterra.png", className="country-flag-large", style={"width": "120px", "height": "auto"}),
        html.Img(src="/assets/España.png", className="country-flag-large", style={"width": "120px", "height": "auto"}),
        html.Img(src="/assets/Italia.png", className="country-flag-large", style={"width": "120px", "height": "auto"}),
        html.Img(src="/assets/Alemania.png", className="country-flag-large", style={"width": "120px", "height": "auto"}),
        html.Img(src="/assets/Francia.png", className="country-flag-large", style={"width": "120px", "height": "auto"}),
    ], className="flags-container-large", style={"marginBottom": "40px"}),
    
    # Botón de Login reubicado entre las banderas y los botones de navegación
    html.Div([
        dbc.Button("LOGIN", id="open-login-button", className="mega-login-button", 
                  size="lg", color="info", style={
                      "fontSize": "2rem", 
                      "padding": "20px 60px",
                      "fontWeight": "bold",
                      "letterSpacing": "3px",
                      "borderRadius": "15px",
                      "boxShadow": "0 8px 25px rgba(0, 0, 0, 0.3)"
                  })
    ], style={"textAlign": "center", "marginBottom": "60px", "marginTop": "20px"}),

    # Botones de Navegación mucho más grandes
    html.Div([
        dbc.Button(
            "DASHBOARD PERFORMANCE", 
            href="/dashboard-performance", 
            color="primary", 
            className="mega-nav-button",
            style={
                "fontSize": "2rem", 
                "padding": "30px 50px",
                "margin": "0 20px",
                "minWidth": "500px",
                "fontWeight": "bold"
            }
        ),
        dbc.Button(
            "DASHBOARD MEDICINA DEPORTIVA", 
            href="/dashboard-medicina", 
            color="info", 
            className="mega-nav-button",
            style={
                "fontSize": "2rem", 
                "padding": "30px 50px",
                "margin": "0 20px",
                "minWidth": "500px",
                "fontWeight": "bold"
            }
        )
    ], className="mega-button-container", style={"display": "flex", "justifyContent": "center", "marginTop": "30px"}),
], style={"height": "100vh", "display": "flex", "flexDirection": "column", "justifyContent": "center"})














