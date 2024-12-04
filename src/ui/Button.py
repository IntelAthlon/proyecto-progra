import pygame
import os

class Button:
    """
    Clase que representa un botón interactivo en la interfaz del juego.

    Atributos:
        text (str): Texto mostrado en el botón.
        rect (pygame.Rect): Rectángulo que define la posición y tamaño del botón.
        callback (function): Función a llamar cuando se presiona el botón.
        sound_manager (SoundManager): Manejador de sonidos del juego.
        type (int): Tipo de botón (0 para normal, 1 para completado).
        color (tuple): Color de fondo del botón.
        text_color (tuple): Color del texto del botón.
        border_color (tuple): Color del borde del botón.
        border_width (int): Ancho del borde del botón.
        font (pygame.font.Font): Fuente utilizada para el texto del botón.
        joystick_connected (bool): Indica si hay un joystick conectado.
    """
    def __init__(self, text, x, y, width, height, callback, sound_manager, joystick, type=0):
        """
        Inicializa una instancia de la clase Button.

        Args:
            text (str): Texto mostrado en el botón.
            x (int): Posición x del botón.
            y (int): Posición y del botón.
            width (int): Ancho del botón.
            height (int): Alto del botón.
            callback (function): Función a llamar cuando se presiona el botón.
            sound_manager (SoundManager): Manejador de sonidos del juego.
            joystick (pygame.joystick.Joystick): Joystick conectado.
            type (int, optional): Tipo de botón (0 para normal, 1 para completado). Por defecto es 0.
        """
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.sound_manager = sound_manager
        self.type = type
        if type == 1:
            self.color = (63, 48, 43)
            self.text_color = (251, 226, 204)
        else:
            self.color = (251, 226, 204)
            self.text_color = (63, 48, 43)
        self.border_color = (63, 48, 43)
        self.border_width = 3
        font_path = os.path.join("assets", "fonts", "newsweekly", "newsweekly-Regular.ttf")
        self.font = pygame.font.Font(font_path, 36)
        self.joystick_connected = False
        if pygame.joystick.get_count() > 0 and joystick is not None:
            self.joystick = joystick
            self.joystick_connected = True

    def draw(self, screen):
        """
        Dibuja el botón en la pantalla.

        Args:
            screen (pygame.Surface): Superficie de la pantalla donde se dibuja el botón.
        """
        pygame.draw.rect(screen, self.border_color, self.rect.inflate(self.border_width * 2, self.border_width * 2), border_radius=10)
        pygame.draw.rect(screen, self.color, self.rect, border_radius=7)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        """
        Maneja los eventos del botón.

        Args:
            event (pygame.event.Event): Evento a manejar.
        """
        mouse_pos = (0,0)
        if self.joystick_connected and event.type == pygame.JOYBUTTONDOWN:
            if self.joystick.get_button(0):
                mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
        if self.rect.collidepoint(mouse_pos):
            if self.sound_manager:
                self.sound_manager.play_sound("select")
            self.callback()