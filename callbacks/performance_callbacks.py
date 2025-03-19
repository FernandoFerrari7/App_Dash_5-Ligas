from dash import Output, Input, callback, html, dcc
import plotly.express as px
import pandas as pd
from utils.data_loader import df

# 🔹 Diccionario de métricas con nombres corregidos
metricas_ofensivas = {
    "Posesión": "Poss",
    "Goles x90": "Per 90 Minutes_Gls",
    "xG x90": "Per 90 Minutes_xG",
    "Progresiones": "Progression"
}

# 🔹 Diccionario de iconos para cada métrica
metricas_iconos = {
    "Posesión": "📊",
    "Goles x90": "⚽",
    "xG x90": "📈",
    "Progresiones": "🚀"
}

# 🔹 Callback para actualizar la lista de equipos (independiente)
@callback(
    Output("dropdown-team", "options"),
    Input("dropdown-league", "value")
)
def actualizar_equipos(liga_seleccionada):
    equipos = df["team"].unique()  # Mostrar los 96 equipos
    return [{"label": equipo, "value": equipo} for equipo in sorted(equipos)]


# 🔹 Callback SOLO para actualizar el gráfico de dispersión
@callback(
    Output("output-graph", "children"),
    [Input("dropdown-metrica", "value"),
     Input("dropdown-league", "value")]
)
def actualizar_grafico(metrica, liga_seleccionada):
    if not metrica:
        return html.P("Selecciona una métrica para visualizar.", className="info-text")

    df_filtrado = df.copy()
    if liga_seleccionada:
        df_filtrado = df_filtrado[df_filtrado["league"] == liga_seleccionada]

    if df_filtrado.empty:
        return html.P("No hay datos disponibles.", className="info-text")

    # 🔹 Elegir ejes del gráfico de dispersión
    if metrica in ["Poss", "Progression"]:
        eje_x, eje_y = "Poss", "Progression"
        title = "Posesión vs. Progresiones"
    else:
        eje_x, eje_y = "Per 90 Minutes_Gls", "Per 90 Minutes_xG"
        title = "Goles x90 vs. xG x90"

    # 🔹 Crear gráfico de dispersión
    fig = px.scatter(
        df_filtrado,
        x=eje_x,
        y=eje_y,
        color="league",
        hover_name="team",
        title=title,
        labels={eje_x: eje_x, eje_y: eje_y},
        template="plotly_dark"
    )
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(height=400, width=900)

    return dcc.Graph(figure=fig)


# 🔹 Callback SOLO para mostrar información del equipo (independiente)
@callback(
    Output("output-team-stats", "children"),
    Input("dropdown-team", "value")
)
def mostrar_estadisticas_equipo(equipo):
    if not equipo:
        return html.Div()

    df_equipo = df[df["team"] == equipo].iloc[0]

    # 🔹 Calcular rankings (general y por liga)
    rankings = {
        metrica: (
            df[metricas_ofensivas[metrica]].rank(ascending=False, method="min")[df["team"] == equipo].values[0],  # Rank Total
            df[df["league"] == df_equipo["league"]][metricas_ofensivas[metrica]].rank(ascending=False, method="min")[df[df["league"] == df_equipo["league"]]["team"] == equipo].values[0]  # Rank Liga
        )
        for metrica in metricas_ofensivas.keys()
    }

    team_stats = html.Div([
        html.H3(f"📊 Estadísticas de {equipo}", className="stats-title"),
        html.Table([
            html.Tr([html.Th("Métrica"), html.Th("Valor"), html.Th("Rank Liga"), html.Th("Rank Total")]),
            *[
                html.Tr([
                    html.Td(f"{metricas_iconos[met]} {met}"),  # ✅ Nombre corregido con icono
                    html.Td(f"{df_equipo[metricas_ofensivas[met]]:.2f}"),
                    html.Td(f"{int(rankings[met][1])}º"),  # Rank dentro de su liga
                    html.Td(f"{int(rankings[met][0])}º")   # Rank total
                ]) for met in metricas_ofensivas.keys()
            ]
        ], className="table table-dark")
    ])
    return team_stats













