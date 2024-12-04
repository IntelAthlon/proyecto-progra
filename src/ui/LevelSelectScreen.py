import pygame
import os

from src.logic.ProgressTracker import ProgressTracker
from src.ui.Button import Button
from src.config import *
import easygui as eg

class LevelSelectScreen:
    """
    Clase que representa la pantalla de selección de nivel del juego.

    Atributos:
        game (Game): Instancia del juego.
        buttons (list): Lista de botones en la pantalla de selección de nivel.
    """
    def __init__(self, game):
        """
        Inicializa una instancia de la clase LevelSelectScreen.

        Args:
            game (Game): Instancia del juego.
        """
        self.game = game
        self.buttons = []
        self.create_level_buttons()
        self.buttons.append(
            Button("Custom", 100, 100, 200, 100, self.start_custom,
                   self.game.sound_manager, self.game.joystick))

    def create_level_buttons(self):
        """
        Crea los botones para seleccionar los niveles del juego.
        """
        screen_width, screen_height = pygame.display.get_surface().get_size()
        button_width, button_height = 50, 50
        padding = 10
        total_width = 10 * (button_width + padding) - padding
        total_height = ((len(self.game.levels) + 9) // 10) * (button_height + padding) - padding
        start_x = (screen_width - total_width) // 2
        start_y = (screen_height - total_height) // 2
        pt = ProgressTracker()
        for i, level_key in enumerate(self.game.levels.keys()):
            row = i // 10
            col = i % 10
            x = start_x + col * (button_width + padding)
            y = start_y + row * (button_width + padding)
            dif = None
            if i + 1 <= 20:
                dif = "easy"
            elif i + 1 <= 40:
                dif = "medium"
            else:
                dif = "hard"
            if pt.is_level_complete(dif, f"level{i + 1}"):
                t = 1
            else:
                t = 0
            self.buttons.append(
                Button(str(i + 1), x, y, button_width, button_height, lambda lk=level_key: self.select_level(lk),
                       self.game.sound_manager, self.game.joystick, t))

    def handle_event(self, event):
        """
        Maneja los eventos de la pantalla de selección de nivel.

        Args:
            event (pygame.event.Event): Evento a manejar.
        """
        if event.type != pygame.JOYAXISMOTION:
            for button in self.buttons:
                button.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.set_screen('menu')

    def draw(self, screen):
        """
        Dibuja la pantalla de selección de nivel.

        Args:
            screen (pygame.Surface): Superficie de la pantalla donde se dibuja la selección de nivel.
        """
        font_path = os.path.join("assets", "fonts", "newsweekly", "newsweekly-Regular.ttf")
        font_size = 64

        border_font = pygame.font.Font(font_path, font_size)
        border_title = border_font.render("Select Level", True, WHITE)
        border_rect = border_title.get_rect(center=((screen.get_width() // 2) + 2, (screen.get_height() // 2) - 198))
        screen.blit(border_title, border_rect)

        font = pygame.font.Font(font_path, font_size)
        title = font.render("Select Level", True, BLACK)
        title_rect = title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 200))
        screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(screen)
    def start_custom(self):
        """
        Inicia un Nonogram personalizado a partir de una imagen seleccionada por el usuario.
        """
        path=eg.fileopenbox()
        if path is None:
            return
        self.game.start_level("custom", path)

    def select_level(self, level_key):
        """
        Selecciona un nivel específico del juego.

        Args:
            level_key (str): Clave del nivel a seleccionar.
        """
        print(f"Cargando el nivel {level_key}")
        self.game.start_level(level_key)

    def update(self):
        """
        Actualiza el estado de la pantalla de selección de nivel.
        """
        self.create_level_buttons()
        pass