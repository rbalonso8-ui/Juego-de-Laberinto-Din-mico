import threading
import time
import random
from Constantes import (
    TIEMPO_INICIAL,
    TIEMPO_AUMENTO_DIFICULTAD,
    DECREMENTO_TIEMPO,
    TIEMPO_MINIMO,
    TIEMPO_APARICION_ELEMENTOS,
    DURACION_ELEMENTOS,
    DIRECCION_ARRIBA, DIRECCION_ABAJO,
    DIRECCION_IZQUIERDA, DIRECCION_DERECHA,
    CELDA_MONEDA_5, CELDA_MONEDA_10,
    CELDA_BOMBA, CELDA_FANTASMA,
    CELDA_LIBRE,
)
from matriz import Matriz
from Jugador import jugador


_TIPOS_ELEMENTOS = [CELDA_MONEDA_5, CELDA_MONEDA_10, CELDA_BOMBA, CELDA_FANTASMA]
_PESOS_ELEMENTOS = [40, 25, 20, 15]

TIEMPO_GRACIA_INICIAL = 4.0


class Juego:
    """Clase principal que maneja la lógica del juego, el estado de la matriz, el jugador y el hilo de desplazamiento."""

    def __init__(self, tamaño):
        """Construye matriz, jugador y deja la partida lista para iniciar."""
        self.tamaño = tamaño
        self.matriz = Matriz(tamaño)
        self.jugador = jugador(tamaño - 1, tamaño // 2)
        self.jugador.bombas = 1
        self.jugador.pasos_fantasma = 1
        self.intervalo_scroll = TIEMPO_INICIAL
        self.jugando = True
        self.lock = threading.Lock()
        self.hilo_scroll = None
        self.tiempo_inicio = None
        self.ultima_aparicion = 0.0
        self.elementos = []
        self._prellenar()

    def _prellenar(self):
        """Llena las filas superiores y coloca un elemento de cada tipo para verlos al iniciar."""
        for fila in range(self.tamaño - 2):
            self.matriz.celdas[fila] = self.matriz.generar_fila()

        libres = self.matriz.obtener_celdas_libres()
        libres = [c for c in libres
                  if c != (self.jugador.fila, self.jugador.columna)]
        random.shuffle(libres)
        ahora = time.time()
        for tipo, (f, c) in zip(_TIPOS_ELEMENTOS, libres):
            self.matriz.valor_celda(f, c, tipo)
            self.elementos.append({'fila': f, 'columna': c, 'tipo': tipo, 't': ahora})

    def iniciar(self):
        """Hace un scroll automático cada intervalo_scroll segundos, y permite procesar teclas para mover al jugador o usar habilidades."""
        self.tiempo_inicio = time.time()
        self.ultima_aparicion = self.tiempo_inicio
        self.hilo_scroll = threading.Thread(
            target=self._bucle_scroll, daemon=True
        )
        self.hilo_scroll.start()

    def detener(self):
        """Marca el juego como terminado para que el scroll salga del bucle."""
        self.jugando = False

    def _bucle_scroll(self):
        """Bucle del scroll secundario: aplica el scroll cada cierto intervalo."""
        time.sleep(TIEMPO_GRACIA_INICIAL)
        while self.jugando:
            with self.lock:
                self.matriz.desplazar_hacia_abajo()
                self.jugador.fila += 1
                vivos = []
                for el in self.elementos:
                    el['fila'] += 1
                    if el['fila'] < self.tamaño:
                        vivos.append(el)
                self.elementos = vivos
                if self.jugador.fila >= self.tamaño:
                    self.jugando = False
                    print("[Game Over] El jugador quedó fuera del mapa.")
                    break
            time.sleep(self.intervalo_scroll)

    def procesar_tecla(self, tecla):
        """Envia una indicacion segun la presionada por el usuario."""
        mapa_direcciones = {
            "Up": DIRECCION_ARRIBA,
            "Down": DIRECCION_ABAJO,
            "Left": DIRECCION_IZQUIERDA,
            "Right": DIRECCION_DERECHA,
        }
        with self.lock:
            if tecla in mapa_direcciones:
                self.jugador.mover(mapa_direcciones[tecla], self.matriz)
            elif tecla == "1":
                self.jugador.usar_bomba(self.matriz)
            elif tecla == "2":
                self.jugador.usar_paso_fantasma(self.matriz)

    def actualizar_tiempos(self):
        """Genera elementos, expira los vencidos y aumenta la dificultad del scroll."""
        if not self.jugando:
            return
        ahora = time.time()
        with self.lock:
            self._expirar_elementos(ahora)
            if ahora - self.ultima_aparicion >= TIEMPO_APARICION_ELEMENTOS:
                self._generar_elemento(ahora)
                self.ultima_aparicion = ahora

            if self.tiempo_inicio is not None:
                transcurrido = ahora - self.tiempo_inicio
                decrementos = int(transcurrido // TIEMPO_AUMENTO_DIFICULTAD)
                nuevo_intervalo = TIEMPO_INICIAL - decrementos * DECREMENTO_TIEMPO
                if nuevo_intervalo < TIEMPO_MINIMO:
                    nuevo_intervalo = TIEMPO_MINIMO
                self.intervalo_scroll = nuevo_intervalo

    def _generar_elemento(self, ahora):
        """Coloca un elemento aleatorio en una celda libre."""
        libres = self.matriz.obtener_celdas_libres()
        libres = [c for c in libres
                  if c != (self.jugador.fila, self.jugador.columna)]
        if not libres:
            return
        f, c = random.choice(libres)
        tipo = random.choices(_TIPOS_ELEMENTOS, weights=_PESOS_ELEMENTOS)[0]
        self.matriz.valor_celda(f, c, tipo)
        self.elementos.append({'fila': f, 'columna': c, 'tipo': tipo, 't': ahora})

    def _expirar_elementos(self, ahora):
        """Elimina elementos vencidos o ya recolectados."""
        sobrevivientes = []
        for el in self.elementos:
            valor_actual = self.matriz.obtener_valor_celda(el['fila'], el['columna'])
            if valor_actual != el['tipo']:
                continue
            if ahora - el['t'] >= DURACION_ELEMENTOS:
                self.matriz.valor_celda(el['fila'], el['columna'], CELDA_LIBRE)
            else:
                sobrevivientes.append(el)
        self.elementos = sobrevivientes