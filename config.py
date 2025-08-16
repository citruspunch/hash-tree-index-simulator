"""
Configuraciones iniciales para el índice hash extensible
"""

# Configuracion de buckets
BUCKET_MAX_SIZE = 4          # Capacidad maxima de cada bucket
INITIAL_LOCAL_DEPTH = 2      # profundidad local inicial de buckets

# Configuracion del directorio  
INITIAL_GLOBAL_DEPTH = 2     # profundidad global inicial (4 entradas)
MINIMUM_GLOBAL_DEPTH = 2     # profundidad minima para shrinking

# Configuracion de claves
MIN_KEY_VALUE = 1            # valor mínimo de clave permitido
MAX_KEY_VALUE = 100          # valor máximo de clave permitido

# configuracion de la interfaz
MENU_OPTIONS = {
    'INSERT': '1',
    'DELETE': '2', 
    'SEARCH': '3',
    'PRINT': '4',
    'EXIT': '5'
}

# Mensajes de la interfaz
MESSAGES = {
    'WELCOME': "Simulador de Índice Hash Extensible",
    'HASH_FUNCTION': "Hash function: h(k) = k",
    'KEY_RANGE': f"Rango de claves: {MIN_KEY_VALUE}-{MAX_KEY_VALUE}",
    'BUCKET_CAPACITY': f"Capacidad de bucket: {BUCKET_MAX_SIZE} claves",
    'GOODBYE': "Fin del simulador.",
    'INVALID_OPTION': "✗ Opción no válida. Seleccione 1-5.",
    'INVALID_NUMBER': "✗ Error: Ingrese un número válido."
}
