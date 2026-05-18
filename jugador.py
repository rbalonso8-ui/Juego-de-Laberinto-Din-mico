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
 
        if not (0 <= nueva_f < matriz.tamaño and 0 <= nueva_c < matriz.tamaño):
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
        
    def usar_bomba(self, matriz):
        """Destruye el obstáculo inmediatamente adyacente en la dirección actual.
 
        Solo se consume una bomba si efectivamente hay un obstáculo en esa celda
        y dentro del mapa. Si no, la habilidad no se gasta.
        """
        if self.bombas <= 0:
            return
        df, dc = self.direccion
        f_obj = self.fila + df
        c_obj = self.columna + dc
        if not (0 <= f_obj < matriz.tamaño and 0 <= c_obj < matriz.tamaño):
            return
        if matriz.obtener_valor_celda(f_obj, c_obj) != CELDA_OBSTACULO:
            return
        matriz.valor_celda(f_obj, c_obj, CELDA_LIBRE)
        self.bombas -= 1
 
    def usar_paso_fantasma(self, matriz):
        """Atraviesa un obstáculo adyacente saltándolo y aterriza 2 casillas adelante.
 
        La celda inmediata debe ser obstáculo y la celda destino debe estar dentro
        del mapa y NO ser otro obstáculo. Si la destino tiene una moneda o poder,
        se recolecta. El obstáculo saltado no se destruye.
        """
        if self.pasos_fantasma <= 0:
            return
        df, dc = self.direccion
        f_obs = self.fila + df
        c_obs = self.columna + dc
        f_dest = self.fila + 2 * df
        c_dest = self.columna + 2 * dc
 
        if matriz.obtener_valor_celda(f_obs, c_obs) != CELDA_OBSTACULO:
            return
        if not (0 <= f_dest < matriz.tamaño and 0 <= c_dest < matriz.tamaño):
            return
        valor_dest = matriz.obtener_valor_celda(f_dest, c_dest)
        if valor_dest == CELDA_OBSTACULO:
            return
 
        self._recolectar(valor_dest)
        matriz.valor_celda(f_dest, c_dest, CELDA_LIBRE)
        self.fila = f_dest
        self.columna = c_dest
        self.pasos_fantasma -= 1