import pandas as pd

def load_data(filepath="data/team_season_stats.csv"):
    """
    Cargar datos desde el CSV y validar las columnas esperadas.
    """
    try:
        df = pd.read_csv(filepath)
        df["Progression"] = df["Progression_PrgC"] + df["Progression_PrgP"]  # 🔹 Sumar progresiones
        print("📂 CSV cargado con éxito.")
    except Exception as e:
        print(f"❌ Error al cargar CSV: {e}")
        df = pd.DataFrame()  # Evitar fallos en el código

    # 🔹 Validar columnas
    columnas_esperadas = {"league", "team", "Poss", "Per 90 Minutes_Gls", "Per 90 Minutes_xG", "Progression"}
    if not columnas_esperadas.issubset(df.columns):
        print("❌ Error: Las columnas esperadas no están en el DataFrame.")
        print("🔎 Columnas disponibles:", df.columns)

    return df

# Cargamos el DataFrame al importar el módulo
df = load_data()

def load_injuries_data(filepath="data/injuries_dataset.csv"):
    """
    Cargar datos de lesiones desde el CSV.
    """
    try:
        df = pd.read_csv(filepath)
        print("📂 CSV de lesiones cargado con éxito.")
        return df
    except Exception as e:
        print(f"❌ Error al cargar CSV de lesiones: {e}")
        # Crear un DataFrame vacío con las columnas esperadas
        columns = ['id', 'equipo', 'liga', 'jugador', 'posicion', 'tipo_lesion', 
                  'area_cuerpo', 'gravedad_dias', 'fecha_lesion', 'fecha_retorno', 
                  'contexto', 'recurrencia', 'tratamiento', 'medico', 'estado']
        return pd.DataFrame(columns=columns)