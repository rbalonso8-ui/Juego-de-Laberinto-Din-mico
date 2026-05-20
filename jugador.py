from Constantes import (
    CELDA_LIBRE, CELDA_OBSTACULO,
    CELDA_MONEDA_5, CELDA_MONEDA_10,
    CELDA_BOMBA, CELDA_FANTASMA,
    PUNTOS_MONEDA_5, PUNTOS_MONEDA_10,
    DIRECCION_ARRIBA,
)
import audio

class jugador:
    """Datos, movimiento y habilidades especiales del jugador."""
    def __init__(self, fila, columna):
        """Crea el jugador en la posición indicada, mirando hacia arriba."""
        self.fila = fila
        self.columna = columna
        self.direccion = DIRECCION_ARRIBA
        self.puntaje = 0
        self.bombas = 0
        self.pasos_fantasma = 0

    def _recolectar(self, valor):
        """Suma el efecto del elemento recolectado al inventario o puntaje."""
        if valor == CELDA_MONEDA_5:
            self.puntaje += PUNTOS_MONEDA_5
            audio.reproducir_moneda()
        elif valor == CELDA_MONEDA_10:
            self.puntaje += PUNTOS_MONEDA_10
            audio.reproducir_moneda()
        elif valor == CELDA_BOMBA:
            self.bombas += 1
        elif valor == CELDA_FANTASMA:
            self.pasos_fantasma += 1

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

        self._recolectar(valor)
        matriz.valor_celda(nueva_f, nueva_c, CELDA_LIBRE)
        self.fila = nueva_f
        self.columna = nueva_c

    def usar_bomba(self, matriz):
        """Destruye el obstáculo inmediatamente adyacente en la dirección actual."""
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
        audio.reproducir_bomba()

    def usar_paso_fantasma(self, matriz):
        """Atraviesa exactamente un obstáculo en la dirección actual y se posiciona en la primera celda libre inmediatamente posterior."""
        if self.pasos_fantasma <= 0:
            return
            
        df, dc = self.direccion
        f1 = self.fila + df
        c1 = self.columna + dc
        
        if not (0 <= f1 < matriz.tamaño and 0 <= c1 < matriz.tamaño):
            return
            
        if matriz.obtener_valor_celda(f1, c1) != CELDA_OBSTACULO:
            return
        f2 = self.fila + df * 2
        c2 = self.columna + dc * 2
        
        if not (0 <= f2 < matriz.tamaño and 0 <= c2 < matriz.tamaño):
            return
            
        valor_destino = matriz.obtener_valor_celda(f2, c2)
        
        if valor_destino == CELDA_OBSTACULO:
            return

        self._recolectar(valor_destino)
        matriz.valor_celda(f2, c2, CELDA_LIBRE)
        
        self.fila = f2
        self.columna = c2
        self.pasos_fantasma -= 1
        audio.reproducir_fantasma()