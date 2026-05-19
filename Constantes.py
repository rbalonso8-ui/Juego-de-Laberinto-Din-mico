import os
import pygame

CELDA_LIBRE = 0
CELDA_OBSTACULO = 1
CELDA_MONEDA_5 = 2
CELDA_MONEDA_10 = 3
CELDA_BOMBA = 4
CELDA_FANTASMA = 5


TAMAÑOS = [10, 20, 30]

TIEMPO_INICIAL = 2.0
TIEMPO_AUMENTO_DIFICULTAD = 15.0
DECREMENTO_TIEMPO = 0.1
TIEMPO_MINIMO = 0.2
TIEMPO_APARICION_ELEMENTOS = 2.5
DURACION_ELEMENTOS = 10.0

PORCENTAJE_OBSTACULOS = 0.40
MAX_LIBRES_CONSECUTIVAS = 2

PUNTOS_MONEDA_5 = 5
PUNTOS_MONEDA_10 = 10


DIRECCION_ARRIBA = (-1, 0)
DIRECCION_ABAJO = (1, 0)
DIRECCION_IZQUIERDA = (0, -1)
DIRECCION_DERECHA = (0, 1)

COLOR_FONDO = "#000000"
COLOR_LIBRE = "#FFDE7A"
COLOR_OBSTACULO = "#310901"
COLOR_JUGADOR = "#0000ff"
COLOR_MONEDA_5 = "#ffd700"
COLOR_MONEDA_10 = "#ff8c00"
COLOR_BOMBA = "#ff0000"
COLOR_FANTASMA = "#9370db"
COLOR_TEXTO = "#ffffff"
COLOR_BORDE = "#0f0f0f"
COLOR_TOP_DESTACADO = "#d7b700"

TAMAÑO_CELDA_PX = 28

ARCHIVO_FONDO = "musica_fondo.ogg" 
ARCHIVO_MONEDA = "moneda.wav"
ARCHIVO_BOMBA = "bomba.wav"
ARCHIVO_FANTASMA = "fantasma.wav"
ARCHIVO_GAME_OVER = "game_over.ogg"

pygame.mixer.init()

CARPETA_SONIDOS = "sonido"

try:
    ruta_fondo = os.path.join(CARPETA_SONIDOS, ARCHIVO_FONDO)
    pygame.mixer.music.load(ruta_fondo)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    sonido_moneda = pygame.mixer.Sound(os.path.join(CARPETA_SONIDOS, ARCHIVO_MONEDA))
    sonido_bomba = pygame.mixer.Sound(os.path.join(CARPETA_SONIDOS, ARCHIVO_BOMBA))
    sonido_fantasma = pygame.mixer.Sound(os.path.join(CARPETA_SONIDOS, ARCHIVO_FANTASMA))
    sonido_game_over = pygame.mixer.Sound(os.path.join(CARPETA_SONIDOS, ARCHIVO_GAME_OVER))

except pygame.error as e:
    print(f"Error al cargar sonidos: {e}")
    sonido_moneda = None
    sonido_bomba = None
    sonido_fantasma = None
    sonido_game_over = None

