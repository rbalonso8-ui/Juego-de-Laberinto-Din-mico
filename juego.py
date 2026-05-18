import threading
import time
import random
from Constantes import TIEMPO_INICIAL, DIRECCION_ARRIBA, DIRECCION_ABAJO, DIRECCION_IZQUIERDA, DIRECCION_DERECHA, CELDA_MONEDA_5, CELDA_MONEDA_10, CELDA_BOMBA, CELDA_FANTASMA
from jugador import jugador
from matriz import Matriz


class Juego:
    """Representa el estado del juego y la logica de actualizacion.
    """

    def __init__(self, tamano):
        self.tamano = tamano
        self.matriz = Matriz(tamano)
        self.jugador = jugador(tamano - 1, tamano // 2)
        self.intervalo_scroll = TIEMPO_INICIAL
        self.jugando = True
        self.lock = threading.Lock()
        self.hilo_scroll = None

        self._prellenar_para_pruebas()

    def _prellenar_para_pruebas(self):
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
        """Arranca el hilo de desplazamiento."""
        self.hilo_scroll = threading.Thread(
            target=self._bucle_scroll, daemon=True
        )
        self.hilo_scroll.start()

    def detener(self):
        self.jugando = False

    def _bucle_scroll(self):
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
        """Hook para subir dificultad y generar elementos.

        Pendiente de implementar en la siguiente iteración.
        """
        pass