
import tkinter as tk
from tkinter import messagebox
from Constantes import CELDA_LIBRE, COLOR_FONDO, COLOR_LIBRE, COLOR_OBSTACULO, COLOR_JUGADOR, COLOR_MONEDA_5, COLOR_MONEDA_10, COLOR_BOMBA, COLOR_FANTASMA, COLOR_TEXTO, COLOR_BORDE, COLOR_TOP_DESTACADO, TAMAÑOS, CELDA_OBSTACULO, CELDA_MONEDA_5, CELDA_MONEDA_10, CELDA_BOMBA, CELDA_FANTASMA, TAMANO_CELDA_PX
class MenuInicial:
    """ Ventana inicial que pide al jugador escoger el tamano de matriz.
    """

    def __init__(self):
        """Construye la ventana de seleccion pero aun no la muestra."""
        self.tamano_seleccionado = None

        self.root = tk.Tk()

        self.root.title("Laberinto Dinamico - Menu Inicial")

        self.root.configure(bg=COLOR_FONDO)

        self.root.resizable(False, False)

        self._construir_widgets()

    def _construir_widgets(self):
        """Crea y posiciona los widgets de la ventana del menu."""
        etiqueta_titulo = tk.Label(
            self.root,
            text="LABERINTO DINAMICO",
            font=("Helvetica", 20, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            pady=10
        )
        
        etiqueta_titulo.pack(padx=20, pady=(15, 5))
        
        etiqueta_instruccion = tk.Label(
            self.root,
            text="Selecciona el tamaño de la matriz:", 
            font=("Helvetica", 12),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        etiqueta_instruccion.pack(pady=(5, 15))

        marco_botones = tk.Frame(self.root, bg=COLOR_FONDO)
        marco_botones.pack(pady=10, padx=30)
        
        for tamano in TAMAÑOS:
            boton = tk.Button(
                marco_botones,
                text=f"{tamano} x {tamano}",
                font=("Helvetica", 14, "bold"),
                width=8,
                height=2,
                bg=COLOR_BORDE,
                fg=COLOR_TEXTO,
                activebackground=COLOR_FONDO,
                activeforeground=COLOR_TEXTO,
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
    
class InterfazJuego:
    """Ventana principal donde transcurre la partida.
    """
 
    def __init__(self, tamaño, juego):
        """Construye la ventana del juego.
 
        Args:
            tamaño (int): Tamaño de la matriz (10/20/30) escogido en el menu.
            juego (Juego): Instancia del motor del juego, ya inicializada.
        """
        self.tamano = tamaño
 
        self.juego = juego

        self._activo = True

        self.root = tk.Tk()

        self.root.title(f"Laberinto Dinamico - {tamaño}x{tamaño}")

        self.root.configure(bg=COLOR_FONDO)

        self.root.resizable(False, False)

        self._construir_widgets()

        self._asociar_teclas()
 
        self.root.protocol("WM_DELETE_WINDOW", self._cerrar)
 
    def _construir_widgets(self):
        """Crea la etiqueta de info, el canvas del tablero y las instrucciones."""
        self.etiqueta_info = tk.Label(
            self.root,
            text="",
            font=("Consolas", 12, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            pady=6
        )

        self.etiqueta_info.pack(fill=tk.X, padx=10, pady=(8, 4))
 
        lado_px = self.tamano * TAMANO_CELDA_PX
 
        self.canvas = tk.Canvas(
            self.root,
            width=lado_px,
            height=lado_px,
            bg=COLOR_FONDO,
            highlightthickness=2,
            highlightbackground=COLOR_BORDE
        )
        self.canvas.pack(padx=10, pady=4)
 
        texto_instrucciones = (
            "Flechas: mover    |    1: bomba    |    "
            "2: paso fantasma    |    Esc: salir"
        )
        etiqueta_instr = tk.Label(
            self.root,
            text=texto_instrucciones,
            font=("Helvetica", 10),
            bg=COLOR_FONDO,
            fg="#aaaaaa",
            pady=4
        )
        etiqueta_instr.pack(fill=tk.X, padx=10, pady=(4, 8))
 
    def _asociar_teclas(self):
        """Conecta cada tecla a la funcion correspondiente del juego."""

        self.root.bind("<Up>",    lambda evento: self._tecla("Up"))
        self.root.bind("<Down>",  lambda evento: self._tecla("Down"))
        self.root.bind("<Left>",  lambda evento: self._tecla("Left"))
        self.root.bind("<Right>", lambda evento: self._tecla("Right"))

        self.root.bind("<Key-1>", lambda evento: self._tecla("1"))
        self.root.bind("<Key-2>", lambda evento: self._tecla("2"))

        self.root.bind("<Escape>", lambda evento: self._cerrar())
 
    def _tecla(self, nombre):
        """Reenvia una pulsacion de tecla al motor del juego.
 
        Args:
            nombre (str): Nombre clave de la tecla ("Up", "Down", "1", etc.).
        """
        if not self.juego.jugando:
            return

        self.juego.procesar_tecla(nombre)

    def iniciar(self):
        """Arranca el juego y entra al mainloop de Tkinter."""
        self.juego.iniciar()
 
        self.root.after(50, self._actualizar)
 
        self.root.mainloop()
 
    def _actualizar(self):
        """Callback periodico: actualiza tiempos, redibuja y reagenda.
 
        Se llama cada INTERVALO_REFRESCO_GUI_MS milisegundos. Si el juego
        ha terminado, en lugar de reagendar mostramos la pantalla final.
        """
        if not self._activo:
            return

        self.juego.actualizar_tiempos()
 
        self._dibujar()
        self._actualizar_info()
 
        if not self.juego.jugando:
            self._mostrar_game_over()
            return
 
        self.root.after(50, self._actualizar)
 
    def _color_para_celda(self, valor):
        """Devuelve el color hex que corresponde a un codigo de celda.
 
        Args:
            valor (int): Codigo de celda (CELDA_LIBRE, CELDA_OBSTACULO, ...).
 
        Returns:
            str: Color en formato hexadecimal "#rrggbb".
        """

        tabla_colores = {
            CELDA_LIBRE:     COLOR_LIBRE,
            CELDA_OBSTACULO: COLOR_OBSTACULO,
            CELDA_MONEDA_5:  COLOR_MONEDA_5,
            CELDA_MONEDA_10: COLOR_MONEDA_10,
            CELDA_BOMBA:     COLOR_BOMBA,
            CELDA_FANTASMA:  COLOR_FANTASMA,
        }

        return tabla_colores.get(valor, COLOR_LIBRE)
 
    def _dibujar(self):
        """Redibuja todo el tablero a partir del estado actual del juego."""
        self.canvas.delete("all")
        with self.juego.lock:

            for fila in range(self.tamano):
                for columna in range(self.tamano):

                    x1 = columna * TAMANO_CELDA_PX
                    y1 = fila * TAMANO_CELDA_PX

                    x2 = x1 + TAMANO_CELDA_PX
                    y2 = y1 + TAMANO_CELDA_PX
 

                    valor = self.juego.matriz.obtener_celda(fila, columna)
                    color = self._color_para_celda(valor)
 

                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=color,
                        outline=COLOR_BORDE,
                        width=1
                    )
 
            f_jug = self.juego.jugador.fila
            c_jug = self.juego.jugador.columna
 
            if 0 <= f_jug < self.tamano and 0 <= c_jug < self.tamano:

                margen = 3
                x1 = c_jug * TAMANO_CELDA_PX + margen
                y1 = f_jug * TAMANO_CELDA_PX + margen
                x2 = (c_jug + 1) * TAMANO_CELDA_PX - margen
                y2 = (f_jug + 1) * TAMANO_CELDA_PX - margen
 
                self.canvas.create_oval(
                    x1, y1, x2, y2,
                    fill=COLOR_JUGADOR,
                    outline=COLOR_BORDE,
                    width=2
                )
 
    def _actualizar_info(self):
        """Refresca el texto del HUD con puntaje, poderes y velocidad."""
        with self.juego.lock:
            puntaje = self.juego.jugador.puntaje
            bombas = self.juego.jugador.bombas
            fantasma = self.juego.jugador.pasos_fantasma
            intervalo = self.juego.intervalo_scroll
 
        texto = (
            f"Puntaje: {puntaje:>5}   |   "
            f"Bombas: {bombas:>2}   |   "
            f"Paso Fantasma: {fantasma:>2}   |   "
            f"Velocidad: {intervalo:.1f}s/fila"
        )
 
        self.etiqueta_info.config(text=texto)
 
    def _cerrar(self):
        """Cierra la ventana del juego deteniendo antes el hilo de scroll."""
        self.juego.detener()

        self._activo = False
 
        try:
            self.root.destroy()
        except tk.TclError:
            pass
        
if __name__ == "__main__":
    menu = MenuInicial()
    tamano = menu.mostrar()

    if tamano is not None:
        from juego import Juego
        juego = Juego(tamano)
        interfaz = InterfazJuego(tamano, juego)
        interfaz.iniciar()