import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Crear la carpeta data si no existe
if not os.path.exists('data'):
    os.makedirs('data')

# Definir los equipos y ligas
leagues = ["ESP-La Liga", "ENG-Premier League", "GER-Bundesliga", "FRA-Ligue 1", "ITA-Serie A"]
teams = {
    "ESP-La Liga": ["Barcelona", "Real Madrid", "Atletico Madrid", "Sevilla", "Valencia", "Real Betis", "Villarreal", "Athletic Bilbao", "Real Sociedad", "Celta Vigo"],
    "ENG-Premier League": ["Manchester City", "Liverpool", "Chelsea", "Arsenal", "Tottenham", "Manchester United", "West Ham", "Leicester City", "Everton", "Newcastle"],
    "GER-Bundesliga": ["Bayern Munich", "Borussia Dortmund", "RB Leipzig", "Bayer Leverkusen", "Eintracht Frankfurt", "Borussia Monchengladbach", "Wolfsburg", "Hoffenheim", "Stuttgart", "Freiburg"],
    "FRA-Ligue 1": ["Paris S-G", "Lille", "Monaco", "Lyon", "Marseille", "Rennes", "Nice", "Strasbourg", "Lens", "Montpellier"],
    "ITA-Serie A": ["Inter", "AC Milan", "Juventus", "Atalanta", "Napoli", "Roma", "Lazio", "Fiorentina", "Bologna", "Sassuolo"]
}

# Definir datos para la generación sintética
positions = ['Portero', 'Defensa Central', 'Lateral Derecho', 'Lateral Izquierdo', 
             'Mediocentro Defensivo', 'Mediocentro', 'Mediocentro Ofensivo', 
             'Extremo Derecho', 'Extremo Izquierdo', 'Delantero Centro']

injury_types = ['Esguince', 'Rotura fibrilar', 'Contusión', 'Fractura', 'Tendinitis',
                'Distensión muscular', 'Lesión de ligamentos', 'Sobrecarga muscular', 
                'Fascitis', 'Pubalgia', 'Luxación']

body_areas = ['Tobillo', 'Rodilla', 'Muslo', 'Isquiotibiales', 'Cuádriceps', 'Gemelo',
              'Tendón de Aquiles', 'Hombro', 'Espalda', 'Cadera', 'Aductor', 'Cabeza',
              'Muñeca', 'Codo']

contexts = ['Partido de Liga', 'Partido de Copa', 'Partido Internacional', 'Entrenamiento',
           'Gimnasio', 'Calentamiento pre-partido']

treatments = ['Fisioterapia', 'Cirugía', 'Reposo', 'Fortalecimiento muscular', 
              'Crioterapia', 'Hidroterapia', 'Terapia de ondas de choque',
              'Rehabilitación funcional', 'PRP', 'Medicación antiinflamatoria']

doctors = ['Dr. García Pérez', 'Dra. Martínez López', 'Dr. Rodríguez Sánchez', 
           'Dra. Fernández Ruiz', 'Dr. González Díaz', 'Dr. Hernández Moya',
           'Dra. López Navarro', 'Dr. Torres Ramos', 'Dra. Sánchez Ortiz']

# Generar nombres para cada equipo
first_names = [
    'Juan', 'Carlos', 'Pedro', 'Luis', 'Miguel', 'Javier', 'Antonio', 'José',
    'John', 'James', 'William', 'Robert', 'Michael', 'David', 'Thomas', 'Richard',
    'Hans', 'Franz', 'Lukas', 'Felix', 'Max', 'Julian', 'Leon', 'Paul',
    'Jean', 'Pierre', 'Nicolas', 'Antoine', 'François', 'Hugo', 'Lucas', 'Theo',
    'Marco', 'Andrea', 'Giuseppe', 'Alessandro', 'Francesco', 'Lorenzo', 'Matteo', 'Luca',
    'Mohammed', 'Ahmed', 'Ali', 'Omar', 'Ibrahim', 'Youssef', 'Karim', 'Hamza'
]

last_names = [
    'García', 'Rodríguez', 'Fernández', 'López', 'Martínez', 'Sánchez', 'Pérez', 'Gómez',
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Wilson',
    'Müller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Meyer', 'Wagner', 'Becker',
    'Dubois', 'Martin', 'Bernard', 'Thomas', 'Petit', 'Robert', 'Richard', 'Durand',
    'Rossi', 'Russo', 'Ferrari', 'Esposito', 'Bianchi', 'Romano', 'Colombo', 'Ricci',
    'Al-Ahmed', 'Al-Saeed', 'Khan', 'Ali', 'Hassan', 'Ibrahim', 'Yousef', 'Mahmoud'
]

# Crear un diccionario de jugadores por equipo
players_by_team = {}
for league in leagues:
    for team in teams[league]:
        # Generar entre 18 y 25 jugadores por equipo
        num_players = random.randint(18, 25)
        team_players = []
        
        for _ in range(num_players):
            player_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            # Evitar duplicados
            while player_name in team_players:
                player_name = f"{random.choice(first_names)} {random.choice(last_names)}"
            team_players.append(player_name)
            
        players_by_team[team] = team_players

# Función para generar fechas de lesión en la temporada 2023-2024
def generate_injury_date():
    start_date = datetime(2023, 8, 1)
    end_date = datetime(2024, 5, 31)
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    return start_date + timedelta(days=random_days)

# Función para calcular fecha de retorno basada en la gravedad
def estimate_return_date(injury_date, severity_days):
    return injury_date + timedelta(days=severity_days)

# Generar dataset de lesiones
injuries_data = []
injury_id = 1

for league in leagues:
    for team in teams[league]:
        # Cada equipo tendrá entre 10 y 25 lesiones durante la temporada
        num_injuries = random.randint(10, 25)
        players = players_by_team[team]
        
        for _ in range(num_injuries):
            # Seleccionar jugador y posición
            player = random.choice(players)
            position = random.choice(positions)
            
            # Generar datos de la lesión
            injury_type = random.choice(injury_types)
            body_area = random.choice(body_areas)
            
            # Severidad basada en el tipo de lesión
            if injury_type in ['Fractura', 'Rotura fibrilar', 'Lesión de ligamentos']:
                severity_days = random.randint(30, 120)  # Lesiones graves
            elif injury_type in ['Esguince', 'Tendinitis', 'Pubalgia']:
                severity_days = random.randint(14, 40)   # Lesiones moderadas
            else:
                severity_days = random.randint(3, 21)    # Lesiones leves
            
            context = random.choice(contexts)
            recurrence = random.choice([True, False, False, False])  # 25% de probabilidad de recurrencia
            treatment = random.choice(treatments)
            doctor = random.choice(doctors)
            
            # Fechas
            injury_date = generate_injury_date()
            return_date = estimate_return_date(injury_date, severity_days)
            
            # Probabilidad de que la lesión esté activa (aún no recuperado)
            is_active = random.random() < 0.15  # 15% de lesiones activas
            if is_active:
                return_date = None
                status = "Activa"
            else:
                status = "Recuperado"
            
            # Crear registro de lesión
            injury = {
                'id': injury_id,
                'equipo': team,
                'liga': league,
                'jugador': player,
                'posicion': position,
                'tipo_lesion': injury_type,
                'area_cuerpo': body_area,
                'gravedad_dias': severity_days,
                'fecha_lesion': injury_date.strftime('%Y-%m-%d'),
                'fecha_retorno': return_date.strftime('%Y-%m-%d') if return_date else None,
                'contexto': context,
                'recurrencia': 'Sí' if recurrence else 'No',
                'tratamiento': treatment,
                'medico': doctor,
                'estado': status
            }
            
            injuries_data.append(injury)
            injury_id += 1

# Crear DataFrame
df_injuries = pd.DataFrame(injuries_data)

# Guardar como CSV
df_injuries.to_csv('data/injuries_dataset.csv', index=False)

# Crear datos adicionales para visualizaciones
# 1. Resumen por equipo
team_summary = df_injuries.groupby('equipo').agg(
    total_lesiones=('id', 'count'),
    dias_baja_promedio=('gravedad_dias', 'mean'),
    lesiones_graves=('gravedad_dias', lambda x: sum(x > 30)),
    lesiones_activas=('estado', lambda x: sum(x == 'Activa'))
).reset_index()

# 2. Resumen por tipo de lesión
injury_type_summary = df_injuries.groupby('tipo_lesion').agg(
    total=('id', 'count'),
    dias_promedio=('gravedad_dias', 'mean')
).reset_index()

# 3. Lesiones por mes
df_injuries['mes'] = pd.to_datetime(df_injuries['fecha_lesion']).dt.strftime('%Y-%m')
lesiones_por_mes = df_injuries['mes'].value_counts().sort_index().reset_index()
lesiones_por_mes.columns = ['mes', 'numero_lesiones']

# Guardar datos procesados
team_summary.to_csv('data/team_injury_summary.csv', index=False)
injury_type_summary.to_csv('data/injury_type_summary.csv', index=False)
lesiones_por_mes.to_csv('data/injuries_by_month.csv', index=False)

print(f"Total de lesiones generadas: {len(df_injuries)}")
print(f"Total de equipos: {len(teams) * len(leagues)}")
print(f"Archivos CSV generados en la carpeta 'data':")
print("- injuries_dataset.csv")
print("- team_injury_summary.csv")
print("- injury_type_summary.csv")
print("- injuries_by_month.csv")