import random
from Constantes import CELDA_LIBRE, CELDA_OBSTACULO, PORCENTAJE_OBSTACULOS, MAX_LIBRES_CONSECUTIVAS


class Matriz:
    """Tablero cuadrado del juego. Se accede como celdas[fila][columna], fila 0 arriba."""

    def __init__(self, tamaño):
        """Crea una matriz cuadrada con todas las celdas libres."""
        self.tamaño = tamaño
        self.celdas = [
            [CELDA_LIBRE for _ in range(tamaño)]
            for _ in range(tamaño)
        ]

    def obtener_valor_celda(self, fila, columna):
        """Devuelve el valor de la celda; None si la posición está fuera de la matriz."""
        if 0 <= fila < self.tamaño and 0 <= columna < self.tamaño:
            return self.celdas[fila][columna]
        return None

    def valor_celda(self, fila, columna, valor):
        """Asigna un nuevo valor a la celda si la posición es válida."""
        if 0 <= fila < self.tamaño and 0 <= columna < self.tamaño:
            self.celdas[fila][columna] = valor

    def generar_fila(self):
        """Genera una fila con exactamente round(N*0.6) obstáculos y máx 2 libres seguidas.

        Coloca el número correcto de cada tipo y mezcla por permutación hasta encontrar
        una ordenación que cumpla la restricción de libres consecutivas.
        """
        n = self.tamaño
        n_obstaculos = round(n * PORCENTAJE_OBSTACULOS)
        fila = [CELDA_OBSTACULO] * n_obstaculos + [CELDA_LIBRE] * (n - n_obstaculos)
        for _ in range(500):
            random.shuffle(fila)
            if self._cumple_restriccion(fila):
                return list(fila)
        return list(fila)

    def _cumple_restriccion(self, fila):
        """True si la fila no tiene más de MAX_LIBRES_CONSECUTIVAS libres seguidas."""
        consec = 0
        for celda in fila:
            if celda == CELDA_LIBRE:
                consec += 1
                if consec > MAX_LIBRES_CONSECUTIVAS:
                    return False
            else:
                consec = 0
        return True

    def desplazar_hacia_abajo(self):
        """Aplica un scroll: elimina la fila inferior, baja todas las demás y agrega una nueva arriba."""
        fila_eliminada = self.celdas[-1]
        fila_nueva = self.generar_fila()
        self.celdas = [fila_nueva] + self.celdas[:-1]
        return fila_eliminada

    def obtener_celdas_libres(self):
        """Devuelve la lista de tuplas (fila, columna) de celdas libres."""
        libres = []
        for f in range(self.tamaño):
            for c in range(self.tamaño):
                if self.celdas[f][c] == CELDA_LIBRE:
                    libres.append((f, c))
        return libres