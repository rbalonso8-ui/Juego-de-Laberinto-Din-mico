import random
import threading

LIBRE = 0
OBSTACULO = 1
JUGADOR = 2
MONEDA_5 = 3
MONEDA_10 = 4
PODER_BOMBA = 5
PODER_FANTASMA = 6
PORCENTAJE_DE_OBSTACULOS = 0.6
MAX_LIBRES_CONSECUTIVAS =2

class Matriz:
    """Representa la el laberinto del juego como una matriz cuadrada
    La matriz se construye progresivamente al inicio de la partida y una vez completa,
    se va desplazando hacia abajo de forma automatica, eliminando la fila inferior y 
    añadiendo una nueva en la parte superior 

    Atributos:
        tamaño (int): El tamaño de la matriz (10, 20 o 30)
        celdas (list[list[int]]): La matriz que representa el laberinto, donde cada celda tiene un numero que representa su estado
        _lock (threading.Lock): Un lock para asegurar que el acceso a la matriz sea seguro desde hilos           
    """
    tamaños_validos = [10,20,30]
    
    def __init__ (self, tamaño):
        """Inicia la matriz con el tamaño indicado se crea una matriz vacia.

        Args:
            tamaño (int): El tamaño de la matriz

        Raises:
            ValueError: Si el tamaño no es válido
        """
        if tamaño not in self.tamaños_validos:
            raise ValueError(f"El tamaño debe ser uno de los siguientes: {self.tamaños_validos}")
        self.tamaño: int = tamaño     
        self.celdas: list[list[int]] = []
        self._lock = threading.Lock()
        
    def generar_fila(self):
        fila: list[int] = []
        consecutivas_libres = 0
 
        for _ in range(self.tamaño):
            if consecutivas_libres >= MAX_LIBRES_CONSECUTIVAS:
                fila.append(OBSTACULO)
                consecutivas_libres = 0
            elif random.random() < PORCENTAJE_DE_OBSTACULOS:
                fila.append(OBSTACULO)
                consecutivas_libres = 0
            else:
                fila.append(LIBRE)
                consecutivas_libres += 1
 
        return fila