import os
 
 
def _ruta(tamaño):
    """Devuelve el nombre del archivo de puntajes para un tamaño de matriz."""
    return f"puntajes_{tamaño}.txt"
 
 
def cargar_puntajes(tamaño):
    """Lee los puntajes guardados para el tamaño dado, ordenados de mayor a menor.
 
    Returns:
        list[int]: lista con hasta 20 puntajes; vacía si no hay archivo.
    """
    ruta = _ruta(tamaño)
    if not os.path.exists(ruta):
        return []
    puntajes = []
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            try:
                puntajes.append(int(linea))
            except ValueError:
                continue
    puntajes.sort(reverse=True)
    return puntajes[:20]
 
 
def guardar_puntaje(tamaño, nuevo_puntaje):
    """Agrega un puntaje al archivo, reordena y conserva sólo el Top 20."""
    puntajes = cargar_puntajes(tamaño)
    puntajes.append(nuevo_puntaje)
    puntajes.sort(reverse=True)
    puntajes = puntajes[:20]
    ruta = _ruta(tamaño)
    with open(ruta, "w", encoding="utf-8") as f:
        for p in puntajes:
            f.write(f"{p}\n")
 
 
def esta_en_top(tamaño, puntaje):
    """True si el puntaje entraría al Top (hay menos de 20 o supera al menor del Top)."""
    puntajes = cargar_puntajes(tamaño)
    if len(puntajes) < 20:
        return True
    return puntaje > puntajes[-1]