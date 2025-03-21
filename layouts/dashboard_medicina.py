from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from components.navbar import sidebar
from utils.data_loader import load_injuries_data

# Cargar los datos de lesiones
df_injuries = load_injuries_data()

# Verificar si hay datos disponibles
if df_injuries.empty:
    print("⚠️ El dataset de lesiones está vacío. Usa primero generate_injuries_data.py para generar los datos.")
    # Opciones predeterminadas para los filtros si no hay datos
    ligas = []
    equipos = []
    tipos_lesion = []
    areas_cuerpo = []
    estados = [{"label": "Activa", "value": "Activa"}, {"label": "Recuperado", "value": "Recuperado"}]
    
    # Layout para cuando no hay datos
    layout = html.Div([
        sidebar,  # Barra lateral
        html.Div([
            html.H1("Dashboard de Medicina Deportiva", className="dashboard-title"),
            html.Div([
                html.Div([
                    html.H3("Datos no disponibles", className="error-title"),
                    html.P([
                        "No se encontró el dataset de lesiones. Por favor, ejecuta primero el script ",
                        html.Code("generate_injuries_data.py"), 
                        " para generar los datos necesarios."
                    ], className="error-message"),
                    html.Pre(
                        "python generate_injuries_data.py", 
                        className="code-block"
                    )
                ], className="error-container")
            ], className="main-content-container-med")
        ], className="dashboard-content")
    ], className="dashboard-container")
    
else:
    # Opciones para filtros si hay datos disponibles
    ligas = [{"label": liga, "value": liga} for liga in sorted(df_injuries["liga"].unique())]
    equipos = [{"label": equipo, "value": equipo} for equipo in sorted(df_injuries["equipo"].unique())]
    tipos_lesion = [{"label": tipo, "value": tipo} for tipo in sorted(df_injuries["tipo_lesion"].unique())]
    areas_cuerpo = [{"label": area, "value": area} for area in sorted(df_injuries["area_cuerpo"].unique())]
    estados = [{"label": "Activa", "value": "Activa"}, {"label": "Recuperado", "value": "Recuperado"}]

    # Layout del Dashboard de Medicina Deportiva con datos
    layout = html.Div([
        sidebar,  # Barra lateral

        html.Div([
            html.H1("Dashboard de Medicina Deportiva", className="dashboard-title"),

            # 🔹 Contenedor de filtros
            html.Div([
                html.Div([
                    html.Label("Liga:", className="label"),
                    dcc.Dropdown(
                        id="dropdown-liga-med",
                        options=ligas,
                        placeholder="Selecciona una liga",
                        className="dropdown"
                    )
                ], className="filter-box"),

                html.Div([
                    html.Label("Equipo:", className="label"),
                    dcc.Dropdown(
                        id="dropdown-equipo-med",
                        options=equipos,
                        placeholder="Selecciona un equipo",
                        className="dropdown"
                    )
                ], className="filter-box"),

                html.Div([
                    html.Label("Tipo de Lesión:", className="label"),
                    dcc.Dropdown(
                        id="dropdown-tipo-lesion",
                        options=tipos_lesion,
                        placeholder="Selecciona un tipo",
                        className="dropdown"
                    )
                ], className="filter-box"),
                
                html.Div([
                    html.Label("Área del Cuerpo:", className="label"),
                    dcc.Dropdown(
                        id="dropdown-area-cuerpo",
                        options=areas_cuerpo,
                        placeholder="Selecciona un área",
                        className="dropdown"
                    )
                ], className="filter-box"),
                
                html.Div([
                    html.Label("Estado:", className="label"),
                    dcc.Dropdown(
                        id="dropdown-estado",
                        options=estados,
                        placeholder="Selecciona un estado",
                        className="dropdown"
                    )
                ], className="filter-box"),
            ], className="filtros-container"),

            # 🔹 Contenedor de tarjetas de resumen
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Lesiones", className="card-title"),
                        html.H2(id="total-lesiones", children="0", className="card-value"),
                    ])
                ], className="summary-card"),
                
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Lesiones Activas", className="card-title"),
                        html.H2(id="lesiones-activas", children="0", className="card-value"),
                    ])
                ], className="summary-card"),
                
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Días de Baja Promedio", className="card-title"),
                        html.H2(id="dias-baja-promedio", children="0", className="card-value"),
                    ])
                ], className="summary-card"),
                
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Lesiones Graves", className="card-title"),
                        html.H2(id="lesiones-graves", children="0", className="card-value"),
                    ])
                ], className="summary-card"),
            ], className="cards-container"),

            # 🔹 Contenedor de gráficos
            html.Div([
                # Primera fila de gráficos
                html.Div([
                    # Gráfico de barras: Lesiones por tipo
                    html.Div([
                        html.H3("Distribución por Tipo de Lesión", className="graph-title"),
                        dcc.Graph(id="grafico-tipos-lesion", figure={})
                    ], className="graph-container-med"),
                    
                    # Gráfico de áreas del cuerpo
                    html.Div([
                        html.H3("Distribución por Área del Cuerpo", className="graph-title"),
                        dcc.Graph(id="grafico-areas-cuerpo", figure={})
                    ], className="graph-container-med"),
                ], className="charts-row"),
                
                # Segunda fila: Gráfico de tendencia + Tabla
                html.Div([
                    # Gráfico de tendencia mensual
                    html.Div([
                        html.H3("Tendencia Mensual de Lesiones", className="graph-title"),
                        dcc.Graph(id="grafico-tendencia-mensual", figure={})
                    ], className="graph-container-med-wide"),
                ], className="charts-row"),
                
                # Tabla interactiva de lesiones
                html.Div([
                    html.H3("Registro Detallado de Lesiones", className="table-title"),
                    dash_table.DataTable(
                        id="tabla-lesiones",
                        columns=[
                            {"name": "ID", "id": "id"},
                            {"name": "Jugador", "id": "jugador"},
                            {"name": "Equipo", "id": "equipo"},
                            {"name": "Posición", "id": "posicion"},
                            {"name": "Tipo de Lesión", "id": "tipo_lesion"},
                            {"name": "Área del Cuerpo", "id": "area_cuerpo"},
                            {"name": "Días de Baja", "id": "gravedad_dias"},
                            {"name": "Fecha Lesión", "id": "fecha_lesion"},
                            {"name": "Fecha Retorno", "id": "fecha_retorno"},
                            {"name": "Estado", "id": "estado"},
                        ],
                        data=[],
                        style_header={
                            'backgroundColor': 'rgba(0, 204, 255, 0.2)',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'textAlign': 'left',
                            'border': '1px solid #222'
                        },
                        style_cell={
                            'backgroundColor': 'rgba(50, 50, 80, 0.2)',
                            'color': 'white',
                            'border': '1px solid #222',
                            'textAlign': 'left',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'maxWidth': 180,
                        },
                        style_data_conditional=[
                            {
                                'if': {'column_id': 'estado', 'filter_query': '{estado} = "Activa"'},
                                'backgroundColor': 'rgba(255, 0, 0, 0.2)',
                                'color': 'white'
                            }
                        ],
                        page_size=10,
                        sort_action='native',
                        filter_action='native',
                        style_table={'overflowX': 'auto'},
                    )
                ], className="table-container"),
            ], className="main-content-container-med"),
        ], className="dashboard-content")
    ], className="dashboard-container")



