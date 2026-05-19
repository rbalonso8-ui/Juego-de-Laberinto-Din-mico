import os

def _ruta(tamaño):
    """Devuelve el nombre del archivo de puntajes para un tamaño de matriz."""
    return f"puntajes_{tamaño}.txt"


def _limpiar_nombre(nombre):
    """Normaliza un nombre: quita tabs/saltos y trunca a 10 caracteres."""
    if not nombre:
        return "Anonimo"
    limpio = nombre.replace("\t", " ").replace("\n", " ").strip()
    if not limpio:
        return "Anonimo"
    return limpio[:10]


def cargar_puntajes(tamaño):
    """Lee los puntajes guardados para el tamaño dado, ordenados de mayor a menor.

    Returns:
        list[tuple[str, int]]: lista con hasta 20 (nombre, puntaje); vacía si no hay archivo.
    """
    ruta = _ruta(tamaño)
    if not os.path.exists(ruta):
        return []
    entradas = []
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.rstrip("\n").rstrip("\r")
            if not linea.strip():
                continue
            if "\t" in linea:
                partes = linea.split("\t", 1)
                nombre = partes[0]
                try:
                    puntaje = int(partes[1])
                except (ValueError, IndexError):
                    continue
            else:
                try:
                    puntaje = int(linea.strip())
                    nombre = "Anonimo"
                except ValueError:
                    continue
            entradas.append((nombre, puntaje))
    entradas.sort(key=lambda x: x[1], reverse=True)
    return entradas[:20]


def guardar_puntaje(tamaño, nombre, puntaje):
    """Agrega un puntaje con nombre, deduplica por nombre y conserva el Top 20."""
    nombre_limpio = _limpiar_nombre(nombre)
    entradas = cargar_puntajes(tamaño)

    mejores = {}
    for n, p in entradas:
        if n not in mejores or p > mejores[n]:
            mejores[n] = p

    if nombre_limpio not in mejores or puntaje > mejores[nombre_limpio]:
        mejores[nombre_limpio] = puntaje

    entradas = sorted(mejores.items(), key=lambda x: x[1], reverse=True)
    entradas = entradas[:20]

    ruta = _ruta(tamaño)
    with open(ruta, "w", encoding="utf-8") as f:
        for n, p in entradas:
            f.write(f"{n}\t{p}\n")


def esta_en_top(tamaño, puntaje):
    """True si el puntaje entraría al Top, hay menos de 20 o supera al menor del Top."""
    puntajes = cargar_puntajes(tamaño)
    if len(puntajes) < 20:
        return True
    return puntaje > puntajes[-1][1]