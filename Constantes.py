# ============================================================
# Tipos de celdas
# ============================================================
CELDA_LIBRE = 0
CELDA_OBSTACULO = 1
CELDA_MONEDA_5 = 2
CELDA_MONEDA_10 = 3
CELDA_BOMBA = 4
CELDA_FANTASMA = 5

# ============================================================
# Tamaños de la matriz
# ============================================================
TAMAÑOS = [10, 20, 30]

# ============================================================
# Tiempos
# ============================================================
TIEMPO_INICIAL = 2.0
TIEMPO_AUMENTO_DIFICULTAD = 15.0
DECREMENTO_TIEMPO = 0.1
TIEMPO_MINIMO = 0.2
TIEMPO_APARICION_ELEMENTOS = 2.5
DURACION_ELEMENTOS = 10.0

# ============================================================
# GGeneración de filas
# ============================================================
PORCENTAJE_OBSTACULOS = 0.60
MAX_LIBRES_CONSECUTIVAS = 2

# ============================================================
# Puntajes
# ============================================================
PUNTOS_MONEDA_5 = 5
PUNTOS_MONEDA_10 = 10

# ============================================================
# Direcciones
# ============================================================
DIRECCION_ARRIBA = (-1, 0)
DIRECCION_ABAJO = (1, 0)
DIRECCION_IZQUIERDA = (0, -1)
DIRECCION_DERECHA = (0, 1)

# ============================================================
# Colores para la GUI
# ============================================================
COLOR_FONDO = "#1e1e1e"
COLOR_LIBRE = "#2d2d2d"
COLOR_OBSTACULO = "#8b4513"
COLOR_JUGADOR = "#00ff00"
COLOR_MONEDA_5 = "#ffd700"
COLOR_MONEDA_10 = "#ff8c00"
COLOR_BOMBA = "#ff3030"
COLOR_FANTASMA = "#9370db"
COLOR_TEXTO = "#ffffff"
COLOR_BORDE = "#0f0f0f"
COLOR_TOP_DESTACADO = "#ffd700"

TAMAÑO_CELDA_PX = 28