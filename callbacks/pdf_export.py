from dash import Output, Input, callback, State, dcc, html
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import base64
import io
from datetime import datetime
import tempfile
import os
from fpdf import FPDF
from utils.data_loader import df

@callback(
    Output("download-pdf", "data"),
    Input("btn-export-pdf", "n_clicks"),
    [State("dropdown-metrica", "value"),
     State("dropdown-league", "value"),
     State("dropdown-team", "value"),
     State("output-graph", "children")],
    prevent_initial_call=True
)
def exportar_a_pdf_profesional(n_clicks, metrica, liga_seleccionada, equipo, graph_children):
    if not n_clicks or not metrica:
        return None

    try:
        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # 🔸 Título sin “STATS” ni “Generado el…”
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Dashboard de Performance', 0, 1, 'C')
        pdf.ln(5)

        # 🔸 Filtros seleccionados
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Filtros aplicados:', 0, 1)

        metricas_nombres = {
            "Poss": "Posesion",
            "Per 90 Minutes_Gls": "Goles x90",
            "Per 90 Minutes_xG": "xG x90",
            "Progression": "Progresiones"
        }

        pdf.set_font('Arial', '', 10)
        pdf.cell(30, 6, 'Metrica:', 0, 0)
        pdf.cell(0, 6, metricas_nombres.get(metrica, metrica), 0, 1)

        if liga_seleccionada:
            pdf.cell(30, 6, 'Liga:', 0, 0)
            pdf.cell(0, 6, liga_seleccionada, 0, 1)

        if equipo:
            pdf.cell(30, 6, 'Equipo:', 0, 0)
            pdf.cell(0, 6, equipo, 0, 1)

        pdf.ln(5)

        if metrica in ["Poss", "Progression"]:
            eje_x, eje_y = "Poss", "Progression"
            title = "Posesion vs. Progresiones"
        else:
            eje_x, eje_y = "Per 90 Minutes_Gls", "Per 90 Minutes_xG"
            title = "Goles x90 vs. xG x90"

        df_filtrado = df.copy()
        if liga_seleccionada:
            df_filtrado = df_filtrado[df_filtrado["league"] == liga_seleccionada]

        fig = go.Figure()
        for liga in df_filtrado["league"].unique():
            df_liga = df_filtrado[df_filtrado["league"] == liga]
            fig.add_trace(go.Scatter(
                x=df_liga[eje_x],
                y=df_liga[eje_y],
                mode='markers',
                marker=dict(size=10),
                name=liga,
                text=df_liga["team"]
            ))

        fig.update_layout(
            title=title,
            xaxis_title=eje_x,
            yaxis_title=eje_y,
            template="plotly_white",
            height=300,   # 🔽 más compacto
            width=600,
            margin=dict(l=30, r=30, t=40, b=30)
        )

        img_bytes = pio.to_image(fig, format="png", scale=2)
        pdf.image_from_bytes(img_bytes, x=30, y=None, w=150)

        # 🔸 No agregamos nueva página
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f'Top 10 - {metricas_nombres.get(metrica, metrica)}', 0, 1)

        pdf.set_font('Arial', 'B', 9)
        pdf.cell(10, 7, 'Pos', 1, 0, 'C')
        pdf.cell(70, 7, 'Equipo', 1, 0, 'C')
        pdf.cell(50, 7, 'Liga', 1, 0, 'C')
        pdf.cell(60, 7, metricas_nombres.get(metrica, metrica), 1, 1, 'C')

        df_top10 = df_filtrado.sort_values(by=metrica, ascending=False).head(10)
        pdf.set_font('Arial', '', 9)
        for i, (_, row) in enumerate(df_top10.iterrows(), 1):
            pdf.cell(10, 6, f'{i}º', 1, 0, 'C')
            pdf.cell(70, 6, row['team'], 1, 0)
            pdf.cell(50, 6, row['league'], 1, 0)
            pdf.cell(60, 6, f'{row[metrica]:.2f}', 1, 1, 'C')

        if equipo and equipo in df["team"].values:
            pdf.ln(8)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, f'Estadisticas detalladas - {equipo}', 0, 1)

            equipo_data = df[df["team"] == equipo].iloc[0]

            pdf.set_font('Arial', 'B', 9)
            pdf.cell(50, 7, 'Metrica', 1, 0, 'C')
            pdf.cell(40, 7, 'Valor', 1, 0, 'C')
            pdf.cell(50, 7, 'Rank Liga', 1, 0, 'C')
            pdf.cell(50, 7, 'Rank Total', 1, 1, 'C')

            pdf.set_font('Arial', '', 9)
            for nombre, nombre_legible in metricas_nombres.items():
                valor = equipo_data[nombre]

                equipo_liga = equipo_data["league"]
                df_liga = df[df["league"] == equipo_liga]

                rank_liga = df_liga[nombre].rank(ascending=False, method="min")[df_liga["team"] == equipo].iloc[0]
                rank_total = df[nombre].rank(ascending=False, method="min")[df["team"] == equipo].iloc[0]

                pdf.cell(50, 6, nombre_legible, 1, 0)
                pdf.cell(40, 6, f'{valor:.2f}', 1, 0, 'C')
                pdf.cell(50, 6, f'{int(rank_liga)}º de {len(df_liga)}', 1, 0, 'C')
                pdf.cell(50, 6, f'{int(rank_total)}º de {len(df)}', 1, 1, 'C')

        # 🔸 Pie de página
        pdf.set_y(-30)
        pdf.set_font('Arial', 'I', 8)
        pdf.cell(0, 10, 'Season 2024-2025', 0, 0, 'C')

        buffer = io.BytesIO()
        buffer.write(pdf.output(dest='S').encode('latin-1'))
        buffer.seek(0)

        fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"dashboard_performance_{fecha_archivo}.pdf"
        if liga_seleccionada:
            nombre_archivo = f"dashboard_{liga_seleccionada.replace(' ', '_')}_{fecha_archivo}.pdf"
        if equipo:
            nombre_archivo = f"dashboard_{equipo.replace(' ', '_')}_{fecha_archivo}.pdf"

        return dcc.send_bytes(buffer.getvalue(), nombre_archivo)

    except Exception as e:
        print(f"Error al generar PDF: {str(e)}")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Error al generar el PDF', 0, 1, 'C')
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f'Se produjo un error: {str(e)}', 0, 1)
        pdf.cell(0, 10, 'Por favor intente nuevamente.', 0, 1)

        buffer = io.BytesIO()
        buffer.write(pdf.output(dest='S').encode('latin-1'))
        buffer.seek(0)
        return dcc.send_bytes(buffer.getvalue(), "error_report.pdf")


class PDF(FPDF):
    def image_from_bytes(self, img_bytes, x=None, y=None, w=0, h=0, type='', link=''):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_file.write(img_bytes)
            temp_name = temp_file.name
        self.image(temp_name, x=x, y=y, w=w, h=h, type=type, link=link)
        try:
            os.unlink(temp_name)
        except:
            pass

