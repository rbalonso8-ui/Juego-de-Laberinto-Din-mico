from gui import MenuInicial, InterfazJuego
from juego import Juego
 
 
def main():
    """Coordina el menú inicial y el inicio de la partida."""
    menu = MenuInicial()
    tamaño = menu.mostrar()
 
    if tamaño is None:
        print("No se seleccionó un tamaño. Saliendo del juego.")
        return
 
    juego = Juego(tamaño)
    interfaz = InterfazJuego(tamaño, juego)
    interfaz.iniciar()
 
    print("Juego finalizado.")
 
 
if __name__ == "__main__":
    main()
 