
import tkinter as tk
from tkinter import messagebox
from Constantes import TAMAÑOS, CELDA_OBSTACULO, CELDA_MONEDA_5, CELDA_MONEDA_10, CELDA_BOMBA,CELDA_FANTASMA
class MenuInicial:
    """ Ventana inicial que pide al jugador escoger el tamano de matriz.
    """

    def __init__(self):
        """Construye la ventana de seleccion pero aun no la muestra."""
        self.tamano_seleccionado = None

        self.root = tk.Tk()

        self.root.title("Laberinto Dinamico - Menu Inicial")

        self.root.configure(bg="#1e1e1e")

        self.root.resizable(False, False)

        self._construir_widgets()

    def _construir_widgets(self):
        """Crea y posiciona los widgets de la ventana del menu."""
        etiqueta_titulo = tk.Label(
            self.root,
            text="LABERINTO DINAMICO",
            font=("Helvetica", 20, "bold"),
            bg="#1e1e1e",
            fg="#FFD900",
            pady=10
        )
        
        etiqueta_titulo.pack(padx=20, pady=(15, 5))
        
        etiqueta_instruccion = tk.Label(
            self.root,
            text="Selecciona el tamaño de la matriz:", 
            font=("Helvetica", 12),
            bg="#1e1e1e",
            fg="#FFD900"
        )
        etiqueta_instruccion.pack(pady=(5, 15))

        marco_botones = tk.Frame(self.root, bg="#1e1e1e")
        marco_botones.pack(pady=10, padx=30)
        
        for tamano in TAMAÑOS:
            boton = tk.Button(
                marco_botones,
                text=f"{tamano} x {tamano}",
                font=("Helvetica", 14, "bold"),
                width=8,
                height=2,
                bg="#3a3a3a",
                fg="#FFD900",
                activebackground="#5a5a5a",
                activeforeground="#FFD900",
                relief="raised",
                cursor="hand2",
                command=lambda t=tamano: self._seleccionar_tamano(t),
            )
            boton.pack(side=tk.LEFT, padx=8, pady=10)

    def _seleccionar_tamano(self, tamano):
        """Callback de los botones del menu. Guarda la seleccion y cierra el menu.

        Args:
            tamano (int): Tamano elegido (10, 20 o 30).
        """
        self.tamano_seleccionado = tamano

        self.root.destroy()

    def mostrar(self):
        """Muestra la ventana y bloquea hasta que el usuario escoja o la cierre.

        Returns:
            int o None: tamano elegido (10/20/30) o None si se cerro la ventana.
        """
        self.root.mainloop()

        return self.tamano_seleccionado
    
if __name__ == "__main__":
    menu = MenuInicial()
    tamano = menu.mostrar()