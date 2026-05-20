import tkinter as tk

from Constantes import (
    CELDA_LIBRE, CELDA_OBSTACULO,
    CELDA_MONEDA_5, CELDA_MONEDA_10,
    CELDA_BOMBA, CELDA_FANTASMA,
    COLOR_FONDO, COLOR_LIBRE, COLOR_OBSTACULO, COLOR_JUGADOR,
    COLOR_MONEDA_5, COLOR_MONEDA_10, COLOR_BOMBA, COLOR_FANTASMA,
    COLOR_TEXTO, COLOR_BORDE, COLOR_TOP_DESTACADO,
    TAMAÑOS, TAMAÑO_CELDA_PX,
)

from puntaje import cargar_puntajes, guardar_puntaje, esta_en_top, nombre_existe

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
        self.root.title("Laberinto Dinamico")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)
        self.construir_widgets()
        
    def tamaño_titulo(self, tamaño):
        """Devuelve el título del juego."""
        if tamaño == 10:
            return ["Facil", "#008400"]
        elif tamaño == 20:
            return ["Medio", "#bebe28"]
        elif tamaño == 30:
            return ["Dificil", "#a52121"]
        else:
            return f"{tamaño}x{tamaño}"

    def construir_widgets(self):
        """Crea y posiciona los widgets de la ventana del menú."""
        tk.Label(
            self.root, text="LABERINTO DINAMICO",
            font=("Helvetica", 20, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO, pady=10,
        ).pack(padx=20, pady=(15, 5))

        tk.Label(
            self.root, text="Selecciona la dificultad:",
            font=("Helvetica", 12), bg=COLOR_FONDO, fg=COLOR_TEXTO,
        ).pack(pady=(5, 15))

        marco = tk.Frame(self.root, bg=COLOR_FONDO)
        marco.pack(pady=10, padx=30)

        for tamaño in TAMAÑOS:
            tk.Button(
                marco, text=f"{self.tamaño_titulo(tamaño)[0]}",
                font=("Helvetica", 14, "bold"),
                width=8, height=2,
                cursor="hand2",
                command=lambda t=tamaño: self.seleccionar_tamaño(t),
                bg = "#4A4A4A",
                fg=self.tamaño_titulo(tamaño)[1],
                activebackground="#5A5A5A",
                activeforeground=self.tamaño_titulo(tamaño)[1],
                relief="flat"
            ).pack(side=tk.LEFT, padx=8, pady=10)

    def seleccionar_tamaño(self, tamaño):
        """Botones del menú, guarda la selección y cierra la ventana."""
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
    """Ventana principal donde transcurre la partida."""

    def __init__(self, tamaño, juego):
        """Construye la ventana del juego con la rejilla de celdas del tablero."""
        self.tamaño = tamaño
        self.juego = juego
        self._activo = True

        self.root = tk.Tk()
        self.root.title(f"Laberinto Dinamico - {self.tamaño_titulo(self.tamaño)[0]}")
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(False, False)

        self._img_celda = tk.PhotoImage(width=1, height=1)
        self.celdas = []
        self._colores_actuales = [
            [None] * self.tamaño for _ in range(self.tamaño)
        ]

        self.construir_widgets()
        self.asociar_teclas()
        self.root.protocol("WM_DELETE_WINDOW", self._cerrar)
        
    def tamaño_titulo(self, tamaño):
        """Devuelve el título del juego."""
        if tamaño == 10:
            return ["Facil", "#00ff00"]
        elif tamaño == 20:
            return ["Medio", "#ffff00"]
        elif tamaño == 30:
            return ["Dificil", "#ff0000"]
        else:
            return f"{tamaño}x{tamaño}"

    def construir_widgets(self):
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
            text="Flechas: mover    |    1: bomba    |    2: paso fantasma ",
            font=("Helvetica", 10),
            bg=COLOR_FONDO, fg="#aaaaaa", pady=4,
        ).pack(fill=tk.X, padx=10, pady=(4, 8))

    def asociar_teclas(self):
        """Conecta cada tecla a la función correspondiente del juego."""
        self.root.bind("<Up>",     lambda e: self.tecla("Up"))
        self.root.bind("<Down>",   lambda e: self.tecla("Down"))
        self.root.bind("<Left>",   lambda e: self.tecla("Left"))
        self.root.bind("<Right>",  lambda e: self.tecla("Right"))
        self.root.bind("<Key-1>",  lambda e: self.tecla("1"))
        self.root.bind("<Key-2>",  lambda e: self.tecla("2"))
        self.root.bind("<Escape>", lambda e: self._cerrar())

    def tecla(self, nombre):
        """Reenvía una señal de tecla al motor del juego."""
        if not self.juego.jugando:
            return
        self.juego.procesar_tecla(nombre)

    def iniciar(self):
        """Arranca el juego y entra al mainloop de Tkinter."""
        self.juego.iniciar()
        self.root.after(50, self.actualizar)
        self.root.mainloop()

    def actualizar(self):
        """actualiza tiempos, redibuja y reagenda."""
        if not self._activo:
            return

        self.juego.actualizar_tiempos()
        self.dibujar()
        self.actualizar_info()

        if not self.juego.jugando:
            self.game_over()
            return

        self.root.after(50, self.actualizar)

    def pintar_celda(self, fila, columna, color):
        """Cambia el color de una celda solo si difiere del actual."""
        if self._colores_actuales[fila][columna] != color:
            self._colores_actuales[fila][columna] = color
            self.celdas[fila][columna].config(bg=color)

    def dibujar(self):
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
                    self.pintar_celda(fila, columna, color)

    def actualizar_info(self):
        """Refresca el texto con puntaje, poderes y velocidad."""
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
                f"Velocidad: {v:.1f}"
            )
        )

    def pedir_nombre(self):
        """Muestra un diálogo modal pidiendo un nombre de máximo 10 caracteres.

        Returns:
            str: nombre ingresado (limitado a 10 caracteres) o "Anonimo" si está vacío.
        """
        nombre_var = tk.StringVar()
        resultado = [None]
 
        dialogo = tk.Toplevel(self.root)
        dialogo.title("¡Top 20!")
        dialogo.configure(bg=COLOR_FONDO)
        dialogo.resizable(False, False)
        dialogo.transient(self.root)
 
        tk.Label(
            dialogo, text="Entraste al Top 20",
            font=("Helvetica", 16, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TOP_DESTACADO,
        ).pack(pady=(20, 5), padx=40)
 
        tk.Label(
            dialogo, text=f"Ingresá tu nombre:",
            font=("Helvetica", 11),
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        ).pack(pady=(0, 10))
        def validar_longitud(P):
            return len(P) <= 10
 
        vcmd = (dialogo.register(validar_longitud), "%P")
        entrada = tk.Entry(
            dialogo, textvariable=nombre_var,
            font=("Consolas", 14),
            width=14, justify="center",
            validate="key", validatecommand=vcmd,
        )
        entrada.pack(pady=(0, 6), padx=20)
        entrada.focus_set()
 
        etiqueta_error = tk.Label(
            dialogo, text="",
            font=("Helvetica", 10, "italic"),
            bg=COLOR_FONDO, fg="#ff6666",
            wraplength=260,
        )
        etiqueta_error.pack(pady=(0, 8), padx=20)
        
        def confirmar(event=None):
            nombre = nombre_var.get().strip()
            if not nombre:
                etiqueta_error.config(text="El nombre no puede estar vacío.")
                return
            nombre = nombre[:10]
            if nombre_existe(self.tamaño, nombre):
                etiqueta_error.config(
                    text=f"El nombre '{nombre}' ya está en el Top. Elegí otro."
                )
                nombre_var.set("")
                entrada.focus_set()
                return
            resultado[0] = nombre
            try:
                dialogo.destroy()
            except tk.TclError:
                pass
 
        tk.Button(
            dialogo, text="Guardar",
            font=("Helvetica", 12, "bold"),
            width=12, cursor="hand2",
            command=confirmar,
        ).pack(pady=(0, 18))
 
        dialogo.bind("<Return>", confirmar)
        dialogo.protocol("WM_DELETE_WINDOW", lambda: None)
        dialogo.update_idletasks()
        try:
            dialogo.grab_set()
        except tk.TclError:
            pass
        dialogo.lift()
        dialogo.focus_force()
 
        self.root.wait_window(dialogo)
        return resultado[0]

    def game_over(self):
        """Muestra una ventana modal con el puntaje final y el Top 20 actualizado."""
        self._activo = False
        puntaje_final = self.juego.jugador.puntaje
        print(f"[Game Over] Puntaje final: {puntaje_final}")

        entra_al_top = esta_en_top(self.tamaño, puntaje_final)

        nombre_propio = None
        if entra_al_top:
            nombre_propio = self.pedir_nombre()
            guardar_puntaje(self.tamaño, nombre_propio, puntaje_final)

        top = cargar_puntajes(self.tamaño)

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
            ventana, text=f"Puntaje final: {puntaje_final}",
            font=("Helvetica", 16, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        ).pack(pady=(0, 8))

        if entra_al_top:
            tk.Label(
                ventana, text=f"Entraste al Top 20 como {nombre_propio}",
                font=("Helvetica", 12, "bold", "italic"),
                bg=COLOR_FONDO, fg=COLOR_TOP_DESTACADO,
            ).pack(pady=(0, 8))
        else:
            tk.Label(
                ventana, text="Seguí intentando para entrar al Top 20",
                font=("Helvetica", 10, "italic"),
                bg=COLOR_FONDO, fg="#aaaaaa",
            ).pack(pady=(0, 8))

        tk.Label(
            ventana, text=f"TOP {20} (matriz {self.tamaño}x{self.tamaño})",
            font=("Helvetica", 12, "bold"),
            bg=COLOR_FONDO, fg=COLOR_TEXTO,
        ).pack(pady=(8, 4))

        marco_top = tk.Frame(ventana, bg=COLOR_FONDO)
        marco_top.pack(padx=30, pady=4)

        propio_marcado = False
        for indice, (nombre_top, valor) in enumerate(top, start=1):
            es_propio = (
                (not propio_marcado)
                and entra_al_top
                and valor == puntaje_final
                and nombre_top == nombre_propio
            )
            if es_propio:
                propio_marcado = True
            flecha = "→" if es_propio else "  "
            texto = f"{flecha} {indice:>2}.   {nombre_top:<10}   {valor}"
            color_fg = COLOR_TOP_DESTACADO if es_propio else COLOR_TEXTO
            tk.Label(
                marco_top, text=texto,
                font=("Consolas", 11, "bold" if es_propio else "normal"),
                bg=COLOR_FONDO, fg=color_fg, anchor="w",
            ).pack(fill=tk.X)

        if len(top) == 0:
            tk.Label(
                marco_top, text="(sin puntajes registrados)",
                font=("Helvetica", 10, "italic"),
                bg=COLOR_FONDO, fg="#888888",
            ).pack()

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
        ).pack(pady=15)

        ventana.protocol("WM_DELETE_WINDOW", cerrar_todo)
        ventana.update_idletasks()
        try:
            ventana.grab_set()
        except tk.TclError:
            pass
        ventana.lift()
        ventana.focus_force()

    def _cerrar(self):
        """Cierra la ventana del juego deteniendo antes el scroll."""
        self.juego.detener()
        self._activo = False
        try:
            self.root.destroy()
        except tk.TclError:
            pass