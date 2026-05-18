import tkinter as tk

from Constantes import (
    CELDA_LIBRE, CELDA_OBSTACULO,
    CELDA_MONEDA_5, CELDA_MONEDA_10,
    CELDA_BOMBA, CELDA_FANTASMA,
    COLOR_FONDO, COLOR_LIBRE, COLOR_OBSTACULO, COLOR_JUGADOR,
    COLOR_MONEDA_5, COLOR_MONEDA_10, COLOR_BOMBA, COLOR_FANTASMA,
    COLOR_TEXTO, COLOR_BORDE,
    TAMAÑOS, TAMAÑO_CELDA_PX,
)


_COLORES = {
    CELDA_LIBRE:     COLOR_LIBRE,
    CELDA_OBSTACULO: COLOR_OBSTACULO,
    CELDA_MONEDA_5:  COLOR_MONEDA_5,
    CELDA_MONEDA_10: COLOR_MONEDA_10,
    CELDA_BOMBA:     COLOR_BOMBA,
    CELDA_FANTASMA:  COLOR_FANTASMA,
}


class MenuInicial:
    """Ventana inicial que pide al jugador escoger el tamaño de la matriz."""

    def __init__(self):
        """Construye la ventana de selección pero aún no la muestra."""
        self.tamaño_seleccionado = None
        self.root = tk.Tk()
        self.root.title("Laberinto Dinamico - Menu Inicial")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)
        self._construir_widgets()

    def _construir_widgets(self):
        """Crea y posiciona los widgets de la ventana del menú."""
        tk.Label(
            self.root, text="LABERINTO DINAMICO",
            font=("Helvetica", 20, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO, pady=10,
        ).pack(padx=20, pady=(15, 5))

        tk.Label(
            self.root, text="Selecciona el tamaño de la matriz:",
            font=("Helvetica", 12), bg=COLOR_FONDO, fg=COLOR_TEXTO,
        ).pack(pady=(5, 15))

        marco = tk.Frame(self.root, bg=COLOR_FONDO)
        marco.pack(pady=10, padx=30)

        for tamaño in TAMAÑOS:
            tk.Button(
                marco, text=f"{tamaño} x {tamaño}",
                font=("Helvetica", 14, "bold"),
                width=8, height=2,
                cursor="hand2",
                command=lambda t=tamaño: self._seleccionar_tamaño(t),
            ).pack(side=tk.LEFT, padx=8, pady=10)

    def _seleccionar_tamaño(self, tamaño):
        """Callback de los botones del menú; guarda la selección y cierra la ventana."""
        self.tamaño_seleccionado = tamaño
        self.root.destroy()

    def mostrar(self):
        """Muestra la ventana y bloquea hasta que el usuario escoja o la cierre.

        Returns:
            int o None: tamaño elegido (10/20/30) o None si se cerró la ventana.
        """
        self.root.mainloop()
        return self.tamaño_seleccionado


class InterfazJuego:
    """Ventana principal donde transcurre la partida (rejilla de celdas)."""

    def __init__(self, tamaño, juego):
        """Construye la ventana del juego con la rejilla de celdas del tablero."""
        self.tamaño = tamaño
        self.juego = juego
        self._activo = True

        self.root = tk.Tk()
        self.root.title(f"Laberinto Dinamico - {tamaño}x{tamaño}")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)

        self._img_celda = tk.PhotoImage(width=1, height=1)
        self.celdas = []
        self._colores_actuales = [
            [None] * self.tamaño for _ in range(self.tamaño)
        ]

        self._construir_widgets()
        self._asociar_teclas()
        self.root.protocol("WM_DELETE_WINDOW", self._cerrar)

    def _construir_widgets(self):
        """Crea la etiqueta de info, la rejilla de celdas y las instrucciones."""
        self.etiqueta_info = tk.Label(
            self.root, text="",
            font=("Consolas", 12, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO, pady=6,
        )
        self.etiqueta_info.pack(fill=tk.X, padx=10, pady=(8, 4))

        marco_tablero = tk.Frame(self.root, bg=COLOR_BORDE, bd=2, relief="sunken")
        marco_tablero.pack(padx=10, pady=4)

        for fila in range(self.tamaño):
            fila_celdas = []
            for columna in range(self.tamaño):
                c = tk.Label(
                    marco_tablero,
                    image=self._img_celda,
                    width=TAMAÑO_CELDA_PX,
                    height=TAMAÑO_CELDA_PX,
                    bg=COLOR_LIBRE,
                    bd=1,
                    relief="raised",
                    highlightthickness=0,
                )
                c.grid(row=fila, column=columna, padx=0, pady=0)
                fila_celdas.append(c)
            self.celdas.append(fila_celdas)

        tk.Label(
            self.root,
            text="Flechas: mover    |    1: bomba    |    2: paso fantasma    |    Esc: salir",
            font=("Helvetica", 10),
            bg=COLOR_FONDO, fg="#aaaaaa", pady=4,
        ).pack(fill=tk.X, padx=10, pady=(4, 8))

    def _asociar_teclas(self):
        """Conecta cada tecla a la función correspondiente del juego."""
        self.root.bind("<Up>",     lambda e: self._tecla("Up"))
        self.root.bind("<Down>",   lambda e: self._tecla("Down"))
        self.root.bind("<Left>",   lambda e: self._tecla("Left"))
        self.root.bind("<Right>",  lambda e: self._tecla("Right"))
        self.root.bind("<Key-1>",  lambda e: self._tecla("1"))
        self.root.bind("<Key-2>",  lambda e: self._tecla("2"))
        self.root.bind("<Escape>", lambda e: self._cerrar())

    def _tecla(self, nombre):
        """Reenvía una pulsación de tecla al motor del juego."""
        if not self.juego.jugando:
            return
        self.juego.procesar_tecla(nombre)

    def iniciar(self):
        """Arranca el juego y entra al mainloop de Tkinter."""
        self.juego.iniciar()
        self.root.after(50, self._actualizar)
        self.root.mainloop()

    def _actualizar(self):
        """Callback periódico: actualiza tiempos, redibuja y reagenda."""
        if not self._activo:
            return

        self.juego.actualizar_tiempos()
        self._dibujar()
        self._actualizar_info()

        if not self.juego.jugando:
            self._mostrar_game_over()
            return

        self.root.after(50, self._actualizar)

    def _pintar_celda(self, fila, columna, color):
        """Cambia el color de una celda solo si difiere del actual."""
        if self._colores_actuales[fila][columna] != color:
            self._colores_actuales[fila][columna] = color
            self.celdas[fila][columna].config(bg=color)

    def _dibujar(self):
        """Redibuja todo el tablero a partir del estado actual del juego."""
        with self.juego.lock:
            f_jug = self.juego.jugador.fila
            c_jug = self.juego.jugador.columna
            for fila in range(self.tamaño):
                for columna in range(self.tamaño):
                    if fila == f_jug and columna == c_jug:
                        color = COLOR_JUGADOR
                    else:
                        valor = self.juego.matriz.obtener_valor_celda(fila, columna)
                        color = _COLORES.get(valor, COLOR_LIBRE)
                    self._pintar_celda(fila, columna, color)

    def _actualizar_info(self):
        """Refresca el texto del HUD con puntaje, poderes y velocidad."""
        with self.juego.lock:
            p = self.juego.jugador.puntaje
            b = self.juego.jugador.bombas
            f = self.juego.jugador.pasos_fantasma
            v = self.juego.intervalo_scroll
        self.etiqueta_info.config(
            text=(
                f"Puntaje: {p:>5}   |   "
                f"Bombas: {b:>2}   |   "
                f"Paso Fantasma: {f:>2}   |   "
                f"Velocidad: {v:.1f}s/fila"
            )
        )

    def _mostrar_game_over(self):
        """Muestra una ventana modal con el puntaje final."""
        self._activo = False
        print(f"[Game Over] Puntaje final: {self.juego.jugador.puntaje}")

        ventana = tk.Toplevel(self.root)
        ventana.title("Game Over")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)
        ventana.transient(self.root)

        tk.Label(
            ventana, text="GAME OVER",
            font=("Helvetica", 26, "bold"),
            bg=COLOR_FONDO, fg="#ff5555",
        ).pack(pady=(20, 5), padx=40)

        tk.Label(
            ventana, text="Quedaste fuera del mapa.",
            font=("Helvetica", 11),
            bg=COLOR_FONDO, fg="#cccccc",
        ).pack(pady=(0, 10))

        tk.Label(
            ventana, text=f"Puntaje final: {self.juego.jugador.puntaje}",
            font=("Helvetica", 16, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        ).pack(pady=(0, 20))

        def cerrar_todo():
            self.juego.detener()
            try:
                ventana.destroy()
            except tk.TclError:
                pass
            try:
                self.root.destroy()
            except tk.TclError:
                pass

        tk.Button(
            ventana, text="Cerrar",
            font=("Helvetica", 12, "bold"),
            width=12,
            cursor="hand2",
            command=cerrar_todo,
        ).pack(pady=(0, 20))

        ventana.protocol("WM_DELETE_WINDOW", cerrar_todo)
        ventana.update_idletasks()
        try:
            ventana.grab_set()
        except tk.TclError:
            pass
        ventana.lift()
        ventana.focus_force()

    def _cerrar(self):
        """Cierra la ventana del juego deteniendo antes el hilo de scroll."""
        self.juego.detener()
        self._activo = False
        try:
            self.root.destroy()
        except tk.TclError:
            pass


if __name__ == "__main__":
    from juego import Juego
    menu = MenuInicial()
    tamaño = menu.mostrar()
    if tamaño is not None:
        juego = Juego(tamaño)
        InterfazJuego(tamaño, juego).iniciar()