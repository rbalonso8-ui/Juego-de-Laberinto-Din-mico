from Constantes import (
    CELDA_LIBRE, CELDA_OBSTACULO,
    CELDA_MONEDA_5, CELDA_MONEDA_10,
    CELDA_BOMBA, CELDA_FANTASMA,
    PUNTOS_MONEDA_5, PUNTOS_MONEDA_10,
    DIRECCION_ARRIBA,
)
 
 
class jugador:
    """Datos y movimiento del jugador."""
 
    def __init__(self, fila, columna):
        """Crea el jugador en la posición indicada, mirando hacia arriba."""
        self.fila = fila
        self.columna = columna
        self.direccion = DIRECCION_ARRIBA
        self.puntaje = 0
        self.bombas = 0
        self.pasos_fantasma = 0
 
    def mover(self, direccion, matriz):
        """Intenta mover al jugador y recolecta el elemento de la celda destino."""
        df, dc = direccion
        self.direccion = direccion
 
        nueva_f = self.fila + df
        nueva_c = self.columna + dc
 
        if not (0 <= nueva_f < matriz.tamano and 0 <= nueva_c < matriz.tamano):
            return
 
        valor = matriz.obtener_valor_celda(nueva_f, nueva_c)
 
        if valor == CELDA_OBSTACULO:
            return
 
        if valor == CELDA_MONEDA_5:
            self.puntaje += PUNTOS_MONEDA_5
        elif valor == CELDA_MONEDA_10:
            self.puntaje += PUNTOS_MONEDA_10
        elif valor == CELDA_BOMBA:
            self.bombas += 1
        elif valor == CELDA_FANTASMA:
            self.pasos_fantasma += 1
 
        matriz.valor_celda(nueva_f, nueva_c, CELDA_LIBRE)
        self.fila = nueva_f
        self.columna = nueva_c