import tkinter as tk
from Constantes import (
    CELDA_LIBRE, CELDA_OBSTACULO,
    CELDA_MONEDA_5, CELDA_MONEDA_10,
    CELDA_BOMBA, CELDA_FANTASMA,
    COLOR_LIBRE, COLOR_OBSTACULO,
    COLOR_MONEDA_5, COLOR_MONEDA_10,
    COLOR_BOMBA, COLOR_FANTASMA, COLOR_JUGADOR,
)
 
 
ESCALA = 4
 
CLAVE_JUGADOR = "JUGADOR"
 
_SPRITE_LIBRE = [
    "FFFFFFF",
    "FFfFFfF",
    "FFFFFFF",
    "FfFFFFf",
    "FFFFFFF",
    "FFfFFfF",
    "FFFFFFF",
]
 
_SPRITE_OBSTACULO = [
    "NNNNNNN",
    "NgNgNgN",
    "NNNNNNN",
    "NgNgNgN",
    "NNNNNNN",
    "NgNgNgN",
    "NNNNNNN",
]
 
_SPRITE_MONEDA_5 = [
    "FFAAAFF",
    "FACCCAF",
    "ACCwCCA",
    "ACwwwCA",
    "ACCwCCA",
    "FACCCAF",
    "FFAAAFF",
]
 
_SPRITE_MONEDA_10 = [
    "FFDDDFF",
    "FDEEEDF",
    "DEwwwED",
    "DEwwwED",
    "DEwwwED",
    "FDEEEDF",
    "FFDDDFF",
]
 
_SPRITE_BOMBA = [
    "FFFyFFF",
    "FFmMmFF",
    "FRRRRRF",
    "RRRsRRR",
    "RRRRRRR",
    "RRRRRRR",
    "FRRRRRF",
]
 
_SPRITE_FANTASMA = [
    "FGGGGGF",
    "GGGGGGG",
    "GGNGNGG",
    "GGGGGGG",
    "GGGGGGG",
    "GGGGGGG",
    "GFGFGFG",
]
 
_SPRITE_JUGADOR = [
    "FBBBBBF",
    "BcccccB",
    "BcNcNcB",
    "BcccccB",
    "BcccccB",
    "BcccccB",
    "FBBBBBF",
]
 
_MAPAS = {
    CELDA_LIBRE: {
        "F": COLOR_LIBRE,
        "f": "#f0e89c"
    },
    CELDA_OBSTACULO: {
        "N": COLOR_OBSTACULO,
        "g": "#3d3d3d"
    },
    CELDA_MONEDA_5: {
        "F": COLOR_LIBRE,
        "A": "#cc7700",
        "C": COLOR_MONEDA_5,
        "w": "#ffffff"
    },
    CELDA_MONEDA_10: {
        "F": COLOR_LIBRE,
        "D": "#8b3a00",
        "E": COLOR_MONEDA_10,
        "w": "#ffe680"
    },
    CELDA_BOMBA: {
        "F": COLOR_LIBRE,
        "y": "#ffd700",
        "M": "#ff8c00",
        "m": "#8b4513",
        "R": COLOR_BOMBA,
        "s": "#ffffff"
    },
    CELDA_FANTASMA: {
        "F": COLOR_LIBRE,
        "G": COLOR_FANTASMA,
        "N": "#000000",
    },
    CLAVE_JUGADOR: {
        "F": COLOR_LIBRE,
        "B": "#0a4d99", 
        "c": COLOR_JUGADOR,
        "N": "#ffffff"
    },
}
 
 
def _crear_image(sprite, mapa_colores):
    """Genera un PhotoImage 7x7 a partir de la matriz de chars y la escala 4x."""
    alto = len(sprite)
    ancho = len(sprite[0])
    img = tk.PhotoImage(width=ancho, height=alto)
    for fila, linea in enumerate(sprite):
        for col, c in enumerate(linea):
            color = mapa_colores.get(c, COLOR_LIBRE)
            img.put(color, to=(col, fila))
    return img.zoom(ESCALA)
 
 
def crear_sprites():
    """Devuelve un dict {clave_tipo: PhotoImage} con todos los sprites.
 
    Las claves son las constantes CELDA_* más la clave especial CLAVE_JUGADOR.
    Llamar SOLO después de haber creado el root de Tk (tk.Tk()).
    """
    sprites_definidos = {
        CELDA_LIBRE:     _SPRITE_LIBRE,
        CELDA_OBSTACULO: _SPRITE_OBSTACULO,
        CELDA_MONEDA_5:  _SPRITE_MONEDA_5,
        CELDA_MONEDA_10: _SPRITE_MONEDA_10,
        CELDA_BOMBA:     _SPRITE_BOMBA,
        CELDA_FANTASMA:  _SPRITE_FANTASMA,
        CLAVE_JUGADOR:   _SPRITE_JUGADOR,
    }
    return {
        clave: _crear_image(sprite, _MAPAS[clave])
        for clave, sprite in sprites_definidos.items()
    }