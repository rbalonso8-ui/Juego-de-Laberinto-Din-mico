import audio
from gui import MenuInicial, InterfazJuego
from juego import Juego
 
 
def main():
    """Coordina el flujo del juuego, menú inicial y el inicio de la partida."""
    audio.iniciar_audio()
    menu = MenuInicial()
    tamaño = menu.mostrar()
 
    if tamaño is None:
        return
 
    juego = Juego(tamaño)
    interfaz = InterfazJuego(tamaño, juego)
    interfaz.iniciar()
 
if __name__ == "__main__":
    main()