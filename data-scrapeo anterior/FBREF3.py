import os
import time
import requests
from bs4 import BeautifulSoup

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
if not os.path.exists("escudos_ligas"):
    os.makedirs("escudos_ligas")

# Iterar sobre cada liga y obtener los escudos
for league, url in leagues.items():
    print(f"\n🔍 Procesando {league}...")
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Crear carpeta de la liga si no existe
        league_folder = os.path.join("escudos_ligas", league)
        if not os.path.exists(league_folder):
            os.makedirs(league_folder)

        # Encontrar las filas de la tabla (equipos)
        rows = soup.find_all("tr")
        
        for row in rows:
            team_cell = row.find("td", {"data-stat": "team"})
            if team_cell:
                # Extraer el nombre del equipo
                team_name = team_cell.find("a").text.strip().replace(" ", "_")
                
                # Extraer la URL del escudo
                img_tag = team_cell.find("img")
                if img_tag:
                    img_url = img_tag["src"]
                    
                    # Descargar la imagen
                    img_response = requests.get(img_url, headers=headers)
                    
                    if img_response.status_code == 200:
                        # Guardar la imagen con el nombre del equipo
                        img_path = os.path.join(league_folder, f"{team_name}.png")
                        with open(img_path, "wb") as file:
                            file.write(img_response.content)
                        
                        print(f"✅ Escudo guardado: {team_name} ({league})")
                    
                    else:
                        print(f"❌ No se pudo descargar el escudo de {team_name}")

        # Pausa entre ligas para evitar bloqueos
        time.sleep(5)

    else:
        print(f"❌ Error al acceder a la página de {league}")

print("\n🎯 ¡Scraping completado con éxito! Los escudos están en la carpeta 'escudos_ligas'.")


