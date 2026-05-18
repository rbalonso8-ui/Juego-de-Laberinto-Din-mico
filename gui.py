import tkinter as tk

from Constantes import CELDA_LIBRE, CELDA_OBSTACULO, CELDA_MONEDA_5, CELDA_MONEDA_10, CELDA_BOMBA, CELDA_FANTASMA, COLOR_FONDO, COLOR_LIBRE, COLOR_OBSTACULO, COLOR_JUGADOR, COLOR_MONEDA_5, COLOR_MONEDA_10, COLOR_BOMBA, COLOR_FANTASMA, COLOR_TEXTO, COLOR_BORDE,TAMAÑOS, TAMANO_CELDA_PX

class MenuInicial:
    """Ventana inicial para escoger tamaño de matriz."""

    def __init__(self):
        self.tamano_seleccionado = None
        self.root = tk.Tk()
        self.root.title("Laberinto Dinamico - Menu Inicial")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)
        self._construir_widgets()

    def _construir_widgets(self):
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

        for tamano in TAMAÑOS:
            tk.Button(
                marco, text=f"{tamano} x {tamano}",
                font=("Helvetica", 14, "bold"),
                width=8, height=2,
                bg=COLOR_BORDE, fg=COLOR_TEXTO,
                activebackground=COLOR_FONDO,
                activeforeground=COLOR_TEXTO,
                relief="raised", cursor="hand2",
                command=lambda t=tamano: self._seleccionar_tamano(t),
            ).pack(side=tk.LEFT, padx=8, pady=10)

    def _seleccionar_tamano(self, tamano):
        self.tamano_seleccionado = tamano
        self.root.destroy()

    def mostrar(self):
        self.root.mainloop()
        return self.tamano_seleccionado


# Mapeo de tipo de celda -> color
_COLORES = {
    CELDA_LIBRE:     COLOR_LIBRE,
    CELDA_OBSTACULO: COLOR_OBSTACULO,
    CELDA_MONEDA_5:  COLOR_MONEDA_5,
    CELDA_MONEDA_10: COLOR_MONEDA_10,
    CELDA_BOMBA:     COLOR_BOMBA,
    CELDA_FANTASMA:  COLOR_FANTASMA,
}


class InterfazJuego:
    """Ventana principal donde transcurre la partida."""

    def __init__(self, tamaño, juego):
        self.tamano = tamaño
        self.juego = juego
        self._activo = True

        self.root = tk.Tk()
        self.root.title(f"Laberinto Dinamico - {tamaño}x{tamaño}")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)

        # Imagen vacía para fijar tamaño en píxeles de los botones de la rejilla
        self._img_celda = tk.PhotoImage(width=1, height=1)

        # Matriz de widgets (botones) y de colores actuales para evitar
        # reconfigurar lo que no cambió.
        self.botones = []
        self._colores_actuales = [
            [None] * self.tamano for _ in range(self.tamano)
        ]

        self._construir_widgets()
        self._asociar_teclas()
        self.root.protocol("WM_DELETE_WINDOW", self._cerrar)

    def _construir_widgets(self):
        self.etiqueta_info = tk.Label(
            self.root, text="",
            font=("Consolas", 12, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO, pady=6,
        )
        self.etiqueta_info.pack(fill=tk.X, padx=10, pady=(8, 4))

        # Marco contenedor del tablero (le da un borde uniforme)
        marco_tablero = tk.Frame(self.root, bg=COLOR_BORDE, bd=2, relief="sunken")
        marco_tablero.pack(padx=10, pady=4)

        # Crear los botones de la rejilla una sola vez. En cada refresco
        # solo cambiamos el bg en lugar de destruir/recrear.
        for fila in range(self.tamano):
            fila_btns = []
            for columna in range(self.tamano):
                b = tk.Button(
                    marco_tablero,
                    image=self._img_celda,
                    width=TAMANO_CELDA_PX,
                    height=TAMANO_CELDA_PX,
                    bg=COLOR_LIBRE,
                    activebackground=COLOR_LIBRE,
                    bd=1,
                    relief="raised",
                    highlightthickness=0,
                    takefocus=0,
                )
                b.grid(row=fila, column=columna, padx=0, pady=0)
                fila_btns.append(b)
            self.botones.append(fila_btns)

        tk.Label(
            self.root,
            text="Flechas: mover    |    1: bomba    |    2: paso fantasma    |    Esc: salir",
            font=("Helvetica", 10),
            bg=COLOR_FONDO, fg="#aaaaaa", pady=4,
        ).pack(fill=tk.X, padx=10, pady=(4, 8))

    def _asociar_teclas(self):
        self.root.bind("<Up>",     lambda e: self._tecla("Up"))
        self.root.bind("<Down>",   lambda e: self._tecla("Down"))
        self.root.bind("<Left>",   lambda e: self._tecla("Left"))
        self.root.bind("<Right>",  lambda e: self._tecla("Right"))
        self.root.bind("<Key-1>",  lambda e: self._tecla("1"))
        self.root.bind("<Key-2>",  lambda e: self._tecla("2"))
        self.root.bind("<Escape>", lambda e: self._cerrar())

    def _tecla(self, nombre):
        if not self.juego.jugando:
            return
        self.juego.procesar_tecla(nombre)

    def iniciar(self):
        self.juego.iniciar()
        self.root.after(50, self._actualizar)
        self.root.mainloop()

    def _actualizar(self):
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
        """Cambia el color de un botón solo si es distinto del actual."""
        if self._colores_actuales[fila][columna] != color:
            self._colores_actuales[fila][columna] = color
            self.botones[fila][columna].config(
                bg=color, activebackground=color
            )

    def _dibujar(self):
        with self.juego.lock:
            f_jug = self.juego.jugador.fila
            c_jug = self.juego.jugador.columna
            for fila in range(self.tamano):
                for columna in range(self.tamano):
                    if fila == f_jug and columna == c_jug:
                        color = COLOR_JUGADOR
                    else:
                        valor = self.juego.matriz.obtener_valor_celda(fila, columna)
                        color = _COLORES.get(valor, COLOR_LIBRE)
                    self._pintar_celda(fila, columna, color)

    def _actualizar_info(self):
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
        self._activo = False
        ventana = tk.Toplevel(self.root)
        ventana.title("Game Over")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)
        ventana.grab_set()

        tk.Label(
            ventana, text="GAME OVER",
            font=("Helvetica", 22, "bold"),
            bg=COLOR_FONDO, fg="#ff5555",
        ).pack(pady=(15, 5), padx=30)

        tk.Label(
            ventana, text=f"Puntaje final: {self.juego.jugador.puntaje}",
            font=("Helvetica", 14, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        ).pack(pady=(0, 15))

        def cerrar_todo():
            self.juego.detener()
            ventana.destroy()
            try:
                self.root.destroy()
            except tk.TclError:
                pass

        tk.Button(
            ventana, text="Cerrar",
            font=("Helvetica", 12, "bold"),
            width=12,
            bg=COLOR_BORDE, fg=COLOR_TEXTO,
            activebackground=COLOR_FONDO, activeforeground=COLOR_TEXTO,
            cursor="hand2",
            command=cerrar_todo,
        ).pack(pady=15)

        ventana.protocol("WM_DELETE_WINDOW", cerrar_todo)

    def _cerrar(self):
        self.juego.detener()
        self._activo = False
        try:
            self.root.destroy()
        except tk.TclError:
            pass


if __name__ == "__main__":
    from juego import Juego
    menu = MenuInicial()
    tamano = menu.mostrar()
    if tamano is not None:
        juego = Juego(tamano)
        InterfazJuego(tamano, juego).iniciar()