# Configuración de la aplicación

# Configuración general
APP_NAME = "Stats Dashboard 2024-2025"
DEBUG = True

# Configuración de seguridad
SECRET_KEY = 'mi_secreto_super_seguro'  # Cambiar en producción a una clave segura

# Configuración de autenticación
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin"
SESSION_TIMEOUT = 600  

# Configuración de rutas protegidas
PROTECTED_ROUTES = [
    '/dashboard-performance',
    '/dashboard-medicina'
]
