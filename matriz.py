import random
from Constantes import CELDA_LIBRE, CELDA_OBSTACULO, PORCENTAJE_OBSTACULOS, MAX_LIBRES_CONSECUTIVAS


class Matriz:
    """Tablero cuadrado del juego. Se accede como celdas[fila][columna], fila 0 arriba."""

    def __init__(self, tamano):
        """Crea una matriz cuadrada con todas las celdas libres."""
        self.tamano = tamano
        self.celdas = [
            [CELDA_LIBRE for _ in range(tamano)]
            for _ in range(tamano)
        ]

    def obtener_valor_celda(self, fila, columna):
        """Devuelve el valor de la celda; None si la posición está fuera de la matriz."""
        if 0 <= fila < self.tamano and 0 <= columna < self.tamano:
            return self.celdas[fila][columna]
        return None

    def valor_celda(self, fila, columna, valor):
        """Asigna un nuevo valor a la celda si la posición es válida."""
        if 0 <= fila < self.tamano and 0 <= columna < self.tamano:
            self.celdas[fila][columna] = valor

    def generar_fila(self):
        """Genera una fila aleatoria con ~60% de obstáculos y máx 2 libres seguidas."""
        nueva_fila = []
        libres_seguidas = 0
        for _ in range(self.tamano):
            if libres_seguidas >= MAX_LIBRES_CONSECUTIVAS:
                nueva_fila.append(CELDA_OBSTACULO)
                libres_seguidas = 0
            else:
                if random.random() < PORCENTAJE_OBSTACULOS:
                    nueva_fila.append(CELDA_OBSTACULO)
                    libres_seguidas = 0
                else:
                    nueva_fila.append(CELDA_LIBRE)
                    libres_seguidas += 1
        return nueva_fila

    def desplazar_hacia_abajo(self):
        """Aplica un scroll: elimina la fila inferior, baja todas las demás y agrega una nueva arriba."""
        fila_eliminada = self.celdas[-1]
        fila_nueva = self.generar_fila()
        self.celdas = [fila_nueva] + self.celdas[:-1]
        return fila_eliminada

    def obtener_celdas_libres(self):
        """Devuelve la lista de tuplas (fila, columna) de celdas libres."""
        libres = []
        for f in range(self.tamano):
            for c in range(self.tamano):
                if self.celdas[f][c] == CELDA_LIBRE:
                    libres.append((f, c))
        return libres