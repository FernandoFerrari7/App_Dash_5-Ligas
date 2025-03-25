# Stats Dashboard 2024-2025

Una aplicación web construida con Dash para visualizar y analizar estadísticas deportivas de las principales ligas europeas.

## Características

- Dashboard de rendimiento para equipos con métricas avanzadas
- Dashboard de medicina deportiva para seguimiento de lesiones
- Autenticación de usuarios
- Exportación de informes a PDF
- Diseño responsive con tema oscuro

## Requisitos

- Python 3.8 o superior
- Pip (gestor de paquetes de Python)

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/FernandoFerrari7/App_Dash_5-Ligas.git
cd stats-dashboard
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Estructura del proyecto

```
stats-dashboard/
├── app.py              # Aplicación principal
├── config.py           # Configuración general
├── assets/             # Archivos estáticos (CSS, imágenes)
├── components/         # Componentes reutilizables
├── data/               # Archivos de datos
├── layouts/            # Layouts para diferentes páginas
├── utils/              # Funciones de utilidad
│   ├── auth.py         # Sistema de autenticación
│   └── data_loader.py  # Cargador de datos
└── scripts/            # Scripts auxiliares
    └── fbref.py        # Script de scraping para obtener datos
```

## Obtención de datos

Antes de ejecutar la aplicación, necesitas obtener los datos estadísticos:

1. Ejecuta el script de scraping para obtener datos de FBREF:
```bash
python scripts/fbref.py
```

Este script generará el archivo `data/team_season_stats.csv` con las estadísticas de los equipos.

2. Para generar los datos simulados de lesiones (opcional):
```bash
python scripts/generate_injuries_data.py
```

Este script generará el archivo `data/injuries_dataset.csv` con datos de lesiones simulados.

## Ejecutar la aplicación

1. Inicia la aplicación:
```bash
python app.py
```

2. Abre tu navegador y visita:
```
http://127.0.0.1:8050/
```

## Acceso al Dashboard

Para acceder a los dashboards protegidos, utiliza las siguientes credenciales:

- Usuario: `admin`
- Contraseña: `admin`

## Despliegue en producción

Para desplegar en producción, se recomienda:

1. Modificar `config.py` cambiando:
   - `DEBUG = False`
   - Actualizar `SECRET_KEY` a una clave segura
   - Configurar credenciales seguras

2. Usar Gunicorn como servidor WSGI:
```bash
gunicorn app:server
```

## Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios importantes antes de enviar un pull request.

