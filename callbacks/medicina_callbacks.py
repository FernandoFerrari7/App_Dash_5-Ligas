from dash import Output, Input, callback, html, dcc, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.data_loader import load_injuries_data

# Cargar datos de lesiones
df_injuries = load_injuries_data()

# Callback para actualizar el dropdown de equipos según la liga seleccionada
@callback(
    Output("dropdown-equipo-med", "options"),
    Input("dropdown-liga-med", "value")
)
def actualizar_equipos_medicina(liga_seleccionada):
    if not liga_seleccionada:
        equipos = df_injuries["equipo"].unique()
    else:
        equipos = df_injuries[df_injuries["liga"] == liga_seleccionada]["equipo"].unique()
    
    return [{"label": equipo, "value": equipo} for equipo in sorted(equipos)]

# Callback para actualizar las tarjetas de resumen
@callback(
    [Output("total-lesiones", "children"),
     Output("lesiones-activas", "children"),
     Output("dias-baja-promedio", "children"),
     Output("lesiones-graves", "children")],
    [Input("dropdown-liga-med", "value"),
     Input("dropdown-equipo-med", "value"),
     Input("dropdown-tipo-lesion", "value"),
     Input("dropdown-area-cuerpo", "value"),
     Input("dropdown-estado", "value")]
)
def actualizar_tarjetas_resumen(liga, equipo, tipo_lesion, area_cuerpo, estado):
    # Filtrar datos según selecciones
    df_filtrado = df_injuries.copy()
    
    if liga:
        df_filtrado = df_filtrado[df_filtrado["liga"] == liga]
    if equipo:
        df_filtrado = df_filtrado[df_filtrado["equipo"] == equipo]
    if tipo_lesion:
        df_filtrado = df_filtrado[df_filtrado["tipo_lesion"] == tipo_lesion]
    if area_cuerpo:
        df_filtrado = df_filtrado[df_filtrado["area_cuerpo"] == area_cuerpo]
    if estado:
        df_filtrado = df_filtrado[df_filtrado["estado"] == estado]
    
    # Calcular estadísticas
    total_lesiones = len(df_filtrado)
    lesiones_activas = df_filtrado[df_filtrado["estado"] == "Activa"].shape[0]
    dias_baja_promedio = round(df_filtrado["gravedad_dias"].mean(), 1) if not df_filtrado.empty else 0
    lesiones_graves = df_filtrado[df_filtrado["gravedad_dias"] > 30].shape[0]
    
    return total_lesiones, lesiones_activas, dias_baja_promedio, lesiones_graves

# Callback para actualizar el gráfico de tipos de lesión
@callback(
    Output("grafico-tipos-lesion", "figure"),
    [Input("dropdown-liga-med", "value"),
     Input("dropdown-equipo-med", "value"),
     Input("dropdown-area-cuerpo", "value"),
     Input("dropdown-estado", "value")]
)
def actualizar_grafico_tipos(liga, equipo, area_cuerpo, estado):
    # Filtrar datos según selecciones
    df_filtrado = df_injuries.copy()
    
    if liga:
        df_filtrado = df_filtrado[df_filtrado["liga"] == liga]
    if equipo:
        df_filtrado = df_filtrado[df_filtrado["equipo"] == equipo]
    if area_cuerpo:
        df_filtrado = df_filtrado[df_filtrado["area_cuerpo"] == area_cuerpo]
    if estado:
        df_filtrado = df_filtrado[df_filtrado["estado"] == estado]
    
    # Agrupar por tipo de lesión
    tipos_count = df_filtrado["tipo_lesion"].value_counts().reset_index()
    tipos_count.columns = ["tipo_lesion", "cantidad"]
    
    # Ordenar por cantidad descendente
    tipos_count = tipos_count.sort_values("cantidad", ascending=False)
    
    # Crear figura
    fig = px.bar(
        tipos_count,
        x="tipo_lesion",
        y="cantidad",
        title="",
        labels={"tipo_lesion": "Tipo de Lesión", "cantidad": "Cantidad"},
        color="cantidad",
        color_continuous_scale="Viridis",
        template="plotly_dark"
    )
    
    fig.update_layout(
        height=400,
        margin=dict(l=40, r=20, t=30, b=40),
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#1a1a2e",
        font=dict(color="white")
    )
    
    return fig

# Callback para actualizar el gráfico de áreas del cuerpo
@callback(
    Output("grafico-areas-cuerpo", "figure"),
    [Input("dropdown-liga-med", "value"),
     Input("dropdown-equipo-med", "value"),
     Input("dropdown-tipo-lesion", "value"),
     Input("dropdown-estado", "value")]
)
def actualizar_grafico_areas(liga, equipo, tipo_lesion, estado):
    # Filtrar datos según selecciones
    df_filtrado = df_injuries.copy()
    
    if liga:
        df_filtrado = df_filtrado[df_filtrado["liga"] == liga]
    if equipo:
        df_filtrado = df_filtrado[df_filtrado["equipo"] == equipo]
    if tipo_lesion:
        df_filtrado = df_filtrado[df_filtrado["tipo_lesion"] == tipo_lesion]
    if estado:
        df_filtrado = df_filtrado[df_filtrado["estado"] == estado]
    
    # Agrupar por área del cuerpo
    areas_count = df_filtrado["area_cuerpo"].value_counts().reset_index()
    areas_count.columns = ["area_cuerpo", "cantidad"]
    
    # Crear figura
    fig = px.pie(
        areas_count,
        values="cantidad",
        names="area_cuerpo",
        title="",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#1a1a2e",
        font=dict(color="white"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

# Callback para actualizar el gráfico de tendencia mensual
@callback(
    Output("grafico-tendencia-mensual", "figure"),
    [Input("dropdown-liga-med", "value"),
     Input("dropdown-equipo-med", "value"),
     Input("dropdown-tipo-lesion", "value"),
     Input("dropdown-area-cuerpo", "value"),
     Input("dropdown-estado", "value")]
)
def actualizar_grafico_tendencia(liga, equipo, tipo_lesion, area_cuerpo, estado):
    # Filtrar datos según selecciones
    df_filtrado = df_injuries.copy()
    
    if liga:
        df_filtrado = df_filtrado[df_filtrado["liga"] == liga]
    if equipo:
        df_filtrado = df_filtrado[df_filtrado["equipo"] == equipo]
    if tipo_lesion:
        df_filtrado = df_filtrado[df_filtrado["tipo_lesion"] == tipo_lesion]
    if area_cuerpo:
        df_filtrado = df_filtrado[df_filtrado["area_cuerpo"] == area_cuerpo]
    if estado:
        df_filtrado = df_filtrado[df_filtrado["estado"] == estado]
    
    # Convertir fecha y agrupar por mes
    df_filtrado["fecha_mes"] = pd.to_datetime(df_filtrado["fecha_lesion"]).dt.strftime("%Y-%m")
    tendencia = df_filtrado["fecha_mes"].value_counts().sort_index().reset_index()
    tendencia.columns = ["mes", "cantidad"]
    
    # Crear figura
    fig = px.line(
        tendencia,
        x="mes",
        y="cantidad",
        title="",
        labels={"mes": "Mes", "cantidad": "Cantidad de Lesiones"},
        markers=True,
        template="plotly_dark"
    )
    
    fig.update_layout(
        height=350,
        margin=dict(l=40, r=20, t=30, b=40),
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="#1a1a2e",
        font=dict(color="white")
    )
    
    return fig

# Callback para actualizar la tabla interactiva
@callback(
    Output("tabla-lesiones", "data"),
    [Input("dropdown-liga-med", "value"),
     Input("dropdown-equipo-med", "value"),
     Input("dropdown-tipo-lesion", "value"),
     Input("dropdown-area-cuerpo", "value"),
     Input("dropdown-estado", "value")]
)
def actualizar_tabla_lesiones(liga, equipo, tipo_lesion, area_cuerpo, estado):
    # Filtrar datos según selecciones
    df_filtrado = df_injuries.copy()
    
    if liga:
        df_filtrado = df_filtrado[df_filtrado["liga"] == liga]
    if equipo:
        df_filtrado = df_filtrado[df_filtrado["equipo"] == equipo]
    if tipo_lesion:
        df_filtrado = df_filtrado[df_filtrado["tipo_lesion"] == tipo_lesion]
    if area_cuerpo:
        df_filtrado = df_filtrado[df_filtrado["area_cuerpo"] == area_cuerpo]
    if estado:
        df_filtrado = df_filtrado[df_filtrado["estado"] == estado]
    
    # Seleccionar y ordenar columnas para la tabla
    cols = ["id", "jugador", "equipo", "posicion", "tipo_lesion", "area_cuerpo", 
            "gravedad_dias", "fecha_lesion", "fecha_retorno", "estado"]
    
    df_tabla = df_filtrado[cols].sort_values(by="fecha_lesion", ascending=False)
    
    return df_tabla.to_dict("records")