import soccerdata as sd
import pandas as pd
import os

try:
    # 🔹 Cargar datos de las 5 grandes ligas europeas para la temporada 2024
    fbref = sd.FBref(leagues="Big 5 European Leagues Combined", seasons=2024)

    # 🔹 Obtener estadísticas de los equipos por temporada
    team_season_stats = fbref.read_team_season_stats(stat_type="standard", opponent_stats=False)

    # 🔹 Restablecer el índice para convertir "league", "season" y "team" en columnas normales, sin agregar extra columnas
    team_season_stats = team_season_stats.reset_index(drop=False)

    # 🔹 Aplanar MultiIndex en columnas si es necesario
    team_season_stats.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in team_season_stats.columns]

    # 🔹 Eliminar la columna "season_"
    team_season_stats = team_season_stats.drop(columns=["season_"], errors='ignore')

    # 🔹 Renombrar columnas:
    # - Eliminar el guion bajo final si lo tienen
    # - Eliminar los prefijos "Playing Time_" y "Performance_"
    team_season_stats.columns = [col.rstrip("_").replace("Playing Time_", "").replace("Performance_", "") for col in team_season_stats.columns]

    # 🔹 Especificar la ruta de la carpeta "data"
    data_dir = r"C:\Users\ferna\OneDrive\Escritorio\Notebooks\Modulo 9\mi_proyecto\data"
    csv_filename = os.path.join(data_dir, "team_season_stats.csv")

    # 🔹 Verificar si el archivo ya existe
    if os.path.exists(csv_filename):
        print(f"⚠ El archivo {csv_filename} ya existe. Se sobrescribirá.")

    # 🔹 Guardar en CSV con formato limpio
    team_season_stats.to_csv(csv_filename, index=False)

    print(f"📂 Archivo guardado como {csv_filename}")

except Exception as e:
    print(f"⚠ Error al procesar los datos: {str(e)}")