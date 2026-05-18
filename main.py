from gui import MenuInicial, InterfazJuego

def main():
    """Funcion principal del programa. Coordina menu inicial e inicio del juego.
    """
    menu = MenuInicial()
    tamaño = menu.mostrar()
 
    if tamaño is None:
        print("No se selecciono un tamaño. Saliendo del juego.")
        return
 
    interfaz = InterfazJuego(tamaño)
    interfaz.iniciar()
    print("Juego finalizado. Hasta la proxima.")
 
if __name__ == "__main__":
    main()