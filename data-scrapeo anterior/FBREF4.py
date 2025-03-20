import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from PIL import Image
import numpy as np
from io import BytesIO

# Diccionario con las ligas y sus URLs
leagues = {
    "Premier_League": "https://fbref.com/es/comps/9/Estadisticas-de-Premier-League",
    "La_Liga": "https://fbref.com/es/comps/12/Estadisticas-de-La-Liga",
    "Serie_A": "https://fbref.com/es/comps/11/Estadisticas-de-Serie-A",
    "Bundesliga": "https://fbref.com/es/comps/20/Estadisticas-de-Bundesliga",
    "Ligue_1": "https://fbref.com/es/comps/13/Estadisticas-de-Ligue-1"
}

# Encabezados para evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Crear carpeta principal si no existe
escudos_dir = "escudos_ligas"
if not os.path.exists(escudos_dir):
    os.makedirs(escudos_dir)

# Diccionario para almacenar las URLs de los escudos
escudos_urls = {}

# Función para eliminar el fondo blanco de la imagen
def remove_white_background(image):
    image = image.convert("RGBA")
    data = np.array(image)

    # Definir el color blanco como fondo
    r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
    white_areas = (r > 200) & (g > 200) & (b > 200)
    
    data[white_areas] = [0, 0, 0, 0]  # Hacerlas transparentes
    return Image.fromarray(data)

# Iterar sobre cada liga y obtener los escudos
for league, url in leagues.items():
    print(f"\n🔍 Procesando {league}...")

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Crear carpeta de la liga si no existe
        league_folder = os.path.join(escudos_dir, league)
        if not os.path.exists(league_folder):
            os.makedirs(league_folder)

        # Encontrar las filas de la tabla (equipos)
        rows = soup.find_all("tr")

        for row in rows:
            team_cell = row.find("td", {"data-stat": "team"})
            if team_cell:
                # Extraer el nombre del equipo
                team_name = team_cell.find("a").text.strip()

                # Extraer la URL del escudo
                img_tag = team_cell.find("img")
                if img_tag:
                    img_url = img_tag["src"]
                    escudos_urls[team_name] = img_url  # Guardar en el diccionario

                    # Descargar la imagen
                    img_response = requests.get(img_url, headers=headers)

                    if img_response.status_code == 200:
                        # Abrir imagen con PIL
                        image = Image.open(BytesIO(img_response.content))
                        image = remove_white_background(image)  # Quitar fondo blanco

                        # Guardar la imagen con el nombre del equipo
                        img_path = os.path.join(league_folder, f"{team_name}.png")
                        image.save(img_path, format="PNG")

                        print(f"✅ Escudo guardado: {team_name} ({league})")

                    else:
                        print(f"❌ No se pudo descargar el escudo de {team_name}")

        # Pausa entre ligas para evitar bloqueos
        time.sleep(5)

    else:
        print(f"❌ Error al acceder a la página de {league}")

print("\n🎯 ¡Scraping completado con éxito! Los escudos están en la carpeta 'escudos_ligas'.")

# 📂 **Actualizar los archivos CSV con la URL de los escudos**
data_dir = r"C:\Users\ferna\OneDrive\Escritorio\Notebooks\Modulo 9\mi_proyecto\data"
csv_path_1 = os.path.join(data_dir, "team_season_stats.csv")
csv_path_2 = os.path.join(data_dir, "team_season_stats_2.csv")

# Cargar los archivos CSV existentes
df1 = pd.read_csv(csv_path_1)
df2 = pd.read_csv(csv_path_2)

# Agregar la columna de URL de escudo a los DataFrames
df1["escudo_url"] = df1["team"].map(escudos_urls)
df2["escudo_url"] = df2["team"].map(escudos_urls)

# Guardar los nuevos archivos con la columna de escudo
csv_output_path_1 = os.path.join(data_dir, "team_season_stats_updated.csv")
csv_output_path_2 = os.path.join(data_dir, "team_season_stats_2_updated.csv")

df1.to_csv(csv_output_path_1, index=False)
df2.to_csv(csv_output_path_2, index=False)

print(f"\n✅ Los archivos actualizados se guardaron en: \n{csv_output_path_1} \n{csv_output_path_2}")
