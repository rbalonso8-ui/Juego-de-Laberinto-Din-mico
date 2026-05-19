import tkinter as tk

def cargar_pixelart():

    pixels = {

        "jugador_hacia_atras1": tk.PhotoImage(
            file="Visual/atras1.png"
        ).zoom(2),

        "jugador_hacia_atras2": tk.PhotoImage(
            file="Visual/atras2.png"
        ).zoom(2),

        "jugador_hacia_delante1": tk.PhotoImage(
            file="Visual/delante1.png"
        ).zoom(2),

        "jugador_hacia_delante2": tk.PhotoImage(
            file="Visual/delante2.png"
        ).zoom(2),

        "jugador_hacia_derecha1": tk.PhotoImage(
            file="Visual/derecha1.png"
        ).zoom(2),

        "jugador_hacia_derecha2": tk.PhotoImage(
            file="Visual/derecha2.png"
        ).zoom(2),

        "jugador_hacia_izquierda1": tk.PhotoImage(
            file="Visual/izquierda1.png"
        ).zoom(2),

        "jugador_hacia_izquierda2": tk.PhotoImage(
            file="Visual/izquierda2.png"
        ).zoom(2),

        "bomba": tk.PhotoImage(
            file="Visual/Bomba.png"
        ).zoom(2),

        "fantasma": tk.PhotoImage(
            file="Visual/Fantasma.png"
        ).zoom(2),

        "moneda10": tk.PhotoImage(
            file="Visual/moneda10.png"
        ).zoom(2),

        "moneda5": tk.PhotoImage(
            file="Visual/moneda5.png"
        ).zoom(2),

        "muro": tk.PhotoImage(
            file="Visual/Muro.png"
        ).zoom(2),

        "suelo": tk.PhotoImage(
            file="Visual/suelo.png"
        ).zoom(2),
    }

    return pixels