import random
from Constantes import CELDA_LIBRE, CELDA_OBSTACULO, PORCENTAJE_OBSTACULOS, MAX_LIBRES_CONSECUTIVAS

 
class Matriz:
    """
    Representa el tablero cuadrado del juego.
 
    Atributos:
        tamano (int): Cantidad de filas (y de columnas) de la matriz. Es cuadrada.
        celdas (list[list[int]]): Estructura bidimensional con el estado de cada celda.
            Se accede como celdas[fila][columna]. La fila 0 esta arriba.
    """
 
    def __init__(self, tamano):
        """
        Constructor: crea una matriz inicialmente vacia (todas las celdas libres).
 
        Args:
            tamano (int): Tamano del lado de la matriz (10, 20 o 30).
        """
        self.tamano = tamano
 
        self.celdas = [
            [CELDA_LIBRE for _ in range(tamano)] 
            for _ in range(tamano) 
        ]
 
    def obtener_valor_celda(self, fila, columna):
        """
        Devuelve el valor (tipo) de la celda en la posicion indicada.
 
        Args:
            fila (int): Indice de fila (0 = arriba).
            columna (int): Indice de columna (0 = izquierda).
 
        Returns:
            int o None: Tipo de celda si la posicion es valida; None si esta fuera.
        """
        if 0 <= fila < self.tamano and 0 <= columna < self.tamano:
            return self.celdas[fila][columna]
        return None
 
    def valor_celda(self, fila, columna, valor):
        """
        Asigna un nuevo valor a la celda indicada.
 
        Args:
            fila (int): Indice de fila.
            columna (int): Indice de columna.
            valor (int): Nuevo tipo de celda (debe ser una de las constantes CELDA_*).
        """
        if 0 <= fila < self.tamano and 0 <= columna < self.tamano:
            self.celdas[fila][columna] = valor
 
    def generar_fila(self):
        """
        Genera una fila aleatoria que cumple las restricciones del enunciado:
        Aproximadamente 60% de obstaculos.
        Nunca mas de 2 celdas libres consecutivas.
 
        Returns:
            list[int]: Lista de tamano N con los valores CELDA_LIBRE o CELDA_OBSTACULO.
        """
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
        """Aplica un scroll:
          - Se elimina la ultima fila.
          - Todas las demas filas bajan una posicion.
          - Se agrega una fila NUEVA generada en la parte SUPERIOR (indice 0).
 
        Returns:
            list[int]: La fila que se elimino, por si se necesita auditarla.
        """
        fila_eliminada = self.celdas[-1]
        fila_nueva = self.generar_fila()
        self.celdas = [fila_nueva] + self.celdas[:-1]
 
        return fila_eliminada
 
    def obtener_celdas_libres(self):
        """Devuelve la lista de coordenadas (fila, columna) que actualmente
        contienen CELDA_LIBRE. La usa el gestor de elementos para escoger
        donde colocar monedas/poderes.
 
        Returns:
            list[tuple[int, int]]: Lista de tuplas (fila, columna).
        """
        libres = []
        for f in range(self.tamano):
            for c in range(self.tamano):
                if self.celdas[f][c] == CELDA_LIBRE:
                    libres.append((f, c))
 
        return libres