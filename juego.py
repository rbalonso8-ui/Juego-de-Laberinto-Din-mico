import threading
import time
import random
from Constantes import (
    TIEMPO_INICIAL,
    DIRECCION_ARRIBA, DIRECCION_ABAJO,
    DIRECCION_IZQUIERDA, DIRECCION_DERECHA,
    CELDA_MONEDA_5, CELDA_MONEDA_10,
    CELDA_BOMBA, CELDA_FANTASMA,
)
from matriz import Matriz
from Jugador import jugador


class Juego:
    """Motor del juego en versión mínima: scroll + movimiento del jugador.

    Pendiente para la siguiente iteración: generación periódica de elementos,
    expiración, aumento de dificultad y poderes (bomba, paso fantasma).
    """

    def __init__(self, tamano):
        """Construye matriz, jugador y deja la partida lista para iniciar."""
        self.tamano = tamano
        self.matriz = Matriz(tamano)
        self.jugador = jugador(tamano - 1, tamano // 2)
        self.intervalo_scroll = TIEMPO_INICIAL
        self.jugando = True
        self.lock = threading.Lock()
        self.hilo_scroll = None
        self._prellenar_para_pruebas()

    def _prellenar_para_pruebas(self):
        """Llena las filas superiores y coloca un elemento de cada tipo para verlos al iniciar."""
        for fila in range(self.tamano - 2):
            self.matriz.celdas[fila] = self.matriz.generar_fila()

        libres = self.matriz.obtener_celdas_libres()
        libres = [c for c in libres
                  if c != (self.jugador.fila, self.jugador.columna)]
        random.shuffle(libres)
        for tipo, (f, c) in zip(
            [CELDA_MONEDA_5, CELDA_MONEDA_10, CELDA_BOMBA, CELDA_FANTASMA],
            libres,
        ):
            self.matriz.valor_celda(f, c, tipo)

    def iniciar(self):
        """Lanza el hilo de desplazamiento (scroll automático)."""
        self.hilo_scroll = threading.Thread(
            target=self._bucle_scroll, daemon=True
        )
        self.hilo_scroll.start()

    def detener(self):
        """Marca el juego como terminado para que el hilo salga del bucle."""
        self.jugando = False

    def _bucle_scroll(self):
        """Bucle del hilo secundario: aplica el scroll cada cierto intervalo."""
        while self.jugando:
            time.sleep(self.intervalo_scroll)
            if not self.jugando:
                break
            with self.lock:
                self.matriz.desplazar_hacia_abajo()
                self.jugador.fila += 1
                if self.jugador.fila >= self.tamano:
                    self.jugando = False
                    break

    def procesar_tecla(self, tecla):
        """Reenvía una pulsación de tecla al jugador (bomba/paso fantasma pendientes)."""
        mapa = {
            "Up": DIRECCION_ARRIBA,
            "Down": DIRECCION_ABAJO,
            "Left": DIRECCION_IZQUIERDA,
            "Right": DIRECCION_DERECHA,
        }
        with self.lock:
            if tecla in mapa:
                self.jugador.mover(mapa[tecla], self.matriz)

    def actualizar_tiempos(self):
        """Hook para subir dificultad y generar elementos. Pendiente de implementar."""
        pass