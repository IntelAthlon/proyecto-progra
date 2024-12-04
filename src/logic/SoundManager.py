import pygame
import pygame.mixer

class SoundManager:
    """
    Clase que maneja los sonidos y la música del juego.

    Atributos:
        sounds (dict): Diccionario que contiene los sonidos del juego.
        music (pygame.mixer.Sound): Objeto de sonido para la música de fondo.
    """
    def __init__(self):
        """
        Inicializa una instancia de la clase SoundManager.
        """
        pygame.mixer.init()
        self.sounds = {
            "select": pygame.mixer.Sound("assets/sounds/select.mp3"),
            "cancel": pygame.mixer.Sound("assets/sounds/cancel.mp3"),
            "complete": pygame.mixer.Sound("assets/sounds/complete.mp3")
        }
        self.music = pygame.mixer.Sound("assets/sounds/back.mp3")

    def play_sound(self, sound_name):
        """
        Reproduce un sonido específico.

        Args:
            sound_name (str): Nombre del sonido a reproducir.
        """
        self.sounds[sound_name].play()

    def play_music(self):
        """
        Reproduce la música de fondo en bucle.
        """
        pygame.mixer.music.load("assets/sounds/back.mp3")
        pygame.mixer.music.play(-1)

    def stop_music(self):
        """
        Detiene la música de fondo.
        """
        pygame.mixer.music.stop()

    def pause_music(self):
        """
        Pausa la música de fondo.
        """
        pygame.mixer.music.pause()

    def resume_music(self):
        """
        Reanuda la música de fondo.
        """
        pygame.mixer.music.unpause()