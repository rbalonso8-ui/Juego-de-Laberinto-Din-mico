from gui import MenuInicial, InterfazJuego

def main():
    """Funcion principal del programa. Coordina menu inicial e inicio del juego.
    """
    menu = MenuInicial()
    tamano = menu.mostrar()
 
    if tamano is None:
        print("No se selecciono un tamano. Saliendo del juego.")
        return
 
    interfaz = InterfazJuego(tamano)
    interfaz.iniciar()
    print("Juego finalizado. Hasta la proxima.")
 
if __name__ == "__main__":
    main()