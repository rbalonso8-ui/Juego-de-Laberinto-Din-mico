import os
try:
    import pygame
    pygame.mixer.init()
    audio_disponible = True
except Exception as e:
    audio_disponible = False

from Constantes import (
    CARPETA_SONIDOS,
    ARCHIVO_FONDO, ARCHIVO_MONEDA, ARCHIVO_BOMBA,
    ARCHIVO_FANTASMA, ARCHIVO_GAME_OVER,
    VOLUMEN_MUSICA_FONDO, VOLUMEN_EFECTOS,
)


_sonido_moneda = None
_sonido_bomba = None
_sonido_fantasma = None
_sonido_game_over = None
_musica_fondo_cargada = False


def _cargar_efecto(nombre_archivo):
    """Carga un archivo de sonido y devuelve el objeto Sound, o None si falla."""
    if not audio_disponible:
        return None
    ruta = os.path.join(CARPETA_SONIDOS, nombre_archivo)
    if not os.path.isfile(ruta):
        return None
    try:
        sonido = pygame.mixer.Sound(ruta)
        sonido.set_volume(VOLUMEN_EFECTOS)
        return sonido
    except Exception as e:
        return None


def iniciar_audio():
    """Carga todos los archivos de sonido y comienza la música de fondo en bucle."""
    global sonido_moneda, sonido_bomba, sonido_fantasma, sonido_game_over
    global _musica_fondo_cargada

    if not audio_disponible:
        return

    sonido_moneda = _cargar_efecto(ARCHIVO_MONEDA)
    sonido_bomba = _cargar_efecto(ARCHIVO_BOMBA)
    sonido_fantasma = _cargar_efecto(ARCHIVO_FANTASMA)
    sonido_game_over = _cargar_efecto(ARCHIVO_GAME_OVER)

    ruta_fondo = os.path.join(CARPETA_SONIDOS, ARCHIVO_FONDO)
    if os.path.isfile(ruta_fondo):
        try:
            pygame.mixer.music.load(ruta_fondo)
            pygame.mixer.music.set_volume(VOLUMEN_MUSICA_FONDO)
            pygame.mixer.music.play(-1) 
            _musica_fondo_cargada = True
        except Exception as e:
            pass


def _reproducir(sonido):
    """Reproduce un efecto si está cargado; ignora silenciosamente si no lo está."""
    if sonido is None:
        return
    try:
        sonido.play()
    except Exception:
        pass


def reproducir_moneda():
    """Reproduce el efecto de recolección de moneda."""
    _reproducir(sonido_moneda)


def reproducir_bomba():
    """Reproduce el efecto de explosión de bomba."""
    _reproducir(sonido_bomba)


def reproducir_fantasma():
    """Reproduce el efecto del paso fantasma."""
    _reproducir(sonido_fantasma)


def reproducir_game_over():
    """Detiene la música de fondo y reproduce el efecto de Game Over."""
    if not audio_disponible:
        return
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass
    _reproducir(sonido_game_over)


def detener_todo():
    """Detiene la música de fondo y libera el mezclador (al cerrar el juego)."""
    if not audio_disponible:
        return
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except Exception:
        pass