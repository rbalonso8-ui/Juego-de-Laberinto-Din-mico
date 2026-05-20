# Juego-de-Laberinto-Din-mico
videojuego con interfaz gráfica utilizando Python, en el cual se apliquen conceptos fundamentales de matrices, programación orientada a objetos, manejo de eventos y concurrencia mediante hilos. El juego consiste en un laberinto dinámico representado mediante una matriz cuadrada, el tamaño podrá ser seleccionado por el usuario al iniciar la partida.

## Controles
Flechas: mover al jugador
1: usar bomba
2: usar paso fantasma
Esc: salir

## Estructura
`main.py` - punto de entrada
`Constantes.py` - configuración
`matriz.py`, `Jugador.py`, `juego.py` - lógica del juego
`gui.py` - interfaz Tkinter
`puntaje.py` - persistencia del Top 20
`audio.py` - música y efectos (requiere pygame)
`sonido/` - archivos de audio