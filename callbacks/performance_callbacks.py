from dash import Output, Input, callback, html, dcc, State
import dash_bootstrap_components as dbc
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

    # 🔹 Crear gráfico de dispersión con tamaño optimizado y centrado
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
    
    # Aumentar el tamaño de los puntos para mejor visibilidad
    fig.update_traces(marker=dict(size=14))
    
    # Configurar el layout del gráfico para que sea apropiado al espacio y centrado
    fig.update_layout(
        # Usar el 100% del espacio disponible
        autosize=True,
        
        # Reducir los márgenes para dar más espacio al gráfico
        margin=dict(l=40, r=40, t=70, b=50),
        
        # Mejorar el título y leyenda
        title=dict(
            text=title,
            font=dict(size=22),
            x=0.5,  # Centrar el título
            xanchor='center',
            y=0.95
        ),
        
        # Optimizar la leyenda
        legend=dict(
            orientation="h",  # Leyenda horizontal
            yanchor="bottom",
            y=1.02,  # Posición sobre el gráfico
            xanchor="right",
            x=1,
            font=dict(size=12)
        ),
        
        # Mejorar el aspecto de los ejes
        xaxis=dict(
            title_font=dict(size=16),
            tickfont=dict(size=12),
            gridcolor='rgba(80, 80, 80, 0.2)',
            showline=True,
            linewidth=1,
            linecolor='rgba(255, 255, 255, 0.3)',
            zeroline=True,
            zerolinecolor='rgba(255, 255, 255, 0.5)'
        ),
        yaxis=dict(
            title_font=dict(size=16),
            tickfont=dict(size=12),
            gridcolor='rgba(80, 80, 80, 0.2)',
            showline=True,
            linewidth=1,
            linecolor='rgba(255, 255, 255, 0.3)',
            zeroline=True,
            zerolinecolor='rgba(255, 255, 255, 0.5)'
        ),
        
        # Colores de fondo
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#1a1a2e",
        
        # Color del texto
        font=dict(color="white")
    )

    # Contenedor con estilos para centrar y ajustar el gráfico perfectamente
    return html.Div(
        dcc.Graph(
            figure=fig, 
            style={
                "height": "100%", 
                "width": "100%",
                "margin": "0 auto",  # Centrar horizontalmente
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center"
            },
            config={
                'displayModeBar': False,  # Ocultar la barra de herramientas
                'responsive': True  # Hacer el gráfico responsivo
            }
        ),
        style={
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "height": "100%",
            "width": "100%"
        }
    )


# 🔹 Callback SOLO para mostrar información del equipo
@callback(
    Output("output-team-stats", "children"),
    [Input("dropdown-metrica", "value"),
     Input("dropdown-league", "value"),
     Input("dropdown-team", "value")]
)
def mostrar_estadisticas_equipo(metrica, liga_seleccionada, equipo):
    # Si no hay métrica seleccionada, mostrar mensaje
    if not metrica:
        return html.Div([
            html.P("Selecciona una métrica para ver el ranking.", className="info-text")
        ])
    
    try:
        # Filtrar por liga si se seleccionó alguna
        df_filtrado = df.copy()
        if liga_seleccionada:
            df_filtrado = df_filtrado[df_filtrado["league"] == liga_seleccionada]
            titulo_liga = f" en {liga_seleccionada}"
        else:
            titulo_liga = " general"
        
        # Asegurarse de que hay datos
        if df_filtrado.empty:
            return html.Div([
                html.P("No hay datos disponibles para los filtros seleccionados.", className="info-text")
            ])
        
        # Obtener el top 10 para la métrica seleccionada
        df_top10 = df_filtrado.sort_values(by=metrica, ascending=False).head(10).reset_index(drop=True)
        
        # Encontrar el nombre amigable de la métrica
        nombre_metrica = next((k for k, v in metricas_ofensivas.items() if v == metrica), metrica)
        
        # Crear tabla de ranking con estilo mejorado
        filas_ranking = []
        for i, row in df_top10.iterrows():
            es_equipo_seleccionado = equipo and row["team"] == equipo
            estilo = {"font-weight": "bold", "color": "#00ccff"} if es_equipo_seleccionado else {}
            
            filas_ranking.append(html.Tr([
                html.Td(f"{i+1}º", className="rank-cell"),
                html.Td(row["team"], className="team-cell", style=estilo),
                html.Td(row["league"]),
                html.Td(f"{row[metrica]:.2f}", style=estilo if es_equipo_seleccionado else {})
            ]))
        
        ranking_tabla = html.Div([
            html.H3(f"🏆 Top 10 - {nombre_metrica}{titulo_liga}", className="stats-title"),
            html.Table([
                html.Thead(html.Tr([
                    html.Th("Pos"),
                    html.Th("Equipo"),
                    html.Th("Liga"),
                    html.Th(nombre_metrica)
                ])),
                html.Tbody(filas_ranking)
            ], className="table table-dark ranking-table")
        ])
        
        # Si hay equipo seleccionado, mostrar sus estadísticas
        if equipo:
            # Verificar si el equipo existe en el dataframe
            if equipo not in df_filtrado["team"].values:
                return html.Div([
                    ranking_tabla,
                    html.Hr(style={"margin": "20px 0"}),
                    html.P(f"No hay datos disponibles para el equipo {equipo} con los filtros seleccionados.", 
                          className="info-text")
                ])
            
            # Obtener datos del equipo
            df_equipo = df[df["team"] == equipo].iloc[0]
            
            # Calcular posición en el ranking actual
            try:
                posicion_actual = df_filtrado[metrica].rank(ascending=False, method="min")[df_filtrado["team"] == equipo].iloc[0]
                total_equipos = len(df_filtrado)
                info_posicion = html.P(f"Posición en ranking actual: {int(posicion_actual)}º de {total_equipos}", 
                                      style={"font-weight": "bold", "color": "#00ccff"})
            except:
                info_posicion = html.P("No se pudo calcular la posición en el ranking.", className="info-text")
            
            # Generar filas para cada métrica
            filas_metricas = []
            for met, met_key in metricas_ofensivas.items():
                # Valor de la métrica
                valor = df_equipo[met_key]
                
                # Calcular ranking en la liga del equipo
                try:
                    equipo_liga = df_equipo["league"]
                    df_liga = df[df["league"] == equipo_liga]
                    rank_liga = df_liga[met_key].rank(ascending=False, method="min")[df_liga["team"] == equipo].iloc[0]
                    rank_liga_texto = f"{int(rank_liga)}º"
                except:
                    rank_liga_texto = "N/A"
                
                # Calcular ranking total
                try:
                    rank_total = df[met_key].rank(ascending=False, method="min")[df["team"] == equipo].iloc[0]
                    rank_total_texto = f"{int(rank_total)}º"
                except:
                    rank_total_texto = "N/A"
                
                # Destacar la métrica actual
                estilo_celda = {"font-weight": "bold", "color": "#00ccff"} if met_key == metrica else {}
                
                filas_metricas.append(html.Tr([
                    html.Td(f"{metricas_iconos[met]} {met}", style=estilo_celda),
                    html.Td(f"{valor:.2f}", style=estilo_celda),
                    html.Td(rank_liga_texto, style=estilo_celda),
                    html.Td(rank_total_texto, style=estilo_celda)
                ]))
            
            # Estadísticas del equipo
            stats_equipo = html.Div([
                html.Hr(style={"margin": "20px 0"}),
                html.H3(f"📊 Estadísticas de {equipo}", className="stats-title"),
                info_posicion,
                html.Table([
                    html.Thead(html.Tr([
                        html.Th("Métrica"),
                        html.Th("Valor"), 
                        html.Th("Rank Liga"), 
                        html.Th("Rank Total")
                    ])),
                    html.Tbody(filas_metricas)
                ], className="table table-dark")
            ])
            
            return html.Div([ranking_tabla, stats_equipo])
        
        return ranking_tabla
        
    except Exception as e:
        # En caso de error, mostrar información del error
        return html.Div([
            html.P(f"Ha ocurrido un error: {str(e)}", className="info-text")
        ])














