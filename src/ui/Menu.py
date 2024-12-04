import pygame
import os
from src.ui.Button import Button
from src.config import *
from sys import exit

class Menu:
    """
    Clase que representa el menú principal del juego.

    Atributos:
        game (Game): Instancia del juego.
        buttons (list): Lista de botones en el menú.
    """
    def __init__(self, game):
        """
        Inicializa una instancia de la clase Menu.

        Args:
            game (Game): Instancia del juego.
        """
        self.game = game
        screen_width, screen_height = pygame.display.get_surface().get_size()
        button_width, button_height = 275, 75
        spacing = 20
        total_height = 2 * button_height + spacing
        start_y = (screen_height - total_height) // 2

        self.buttons = [
            Button("Seleccionar nivel", (screen_width - button_width) // 2, start_y + 20, button_width, button_height,
                   self.select_level, self.game.sound_manager, self.game.joystick),
            Button("Salir", (screen_width - button_width) // 2, start_y + button_height + spacing + 20, button_width,
                   button_height, self.quit_game, self.game.sound_manager, self.game.joystick)
        ]

    def handle_event(self, event):
        """
        Maneja los eventos del menú.

        Args:
            event (pygame.event.Event): Evento a manejar.
        """
        for button in self.buttons:
            button.handle_event(event)

    def draw(self, screen):
        """
        Dibuja el menú en la pantalla.

        Args:
            screen (pygame.Surface): Superficie de la pantalla donde se dibuja el menú.
        """
        font_path =  os.path.join("assets", "fonts", "newsweekly", "newsweekly-Regular.ttf")
        font_size = 128
        border_size = 3

        border_font = pygame.font.Font(font_path, font_size)
        border_title = border_font.render("AtomicGram", True, WHITE)
        border_rect = border_title.get_rect(center=((screen.get_width() // 2) + 2, (screen.get_height() // 2) - 163))
        screen.blit(border_title, border_rect)

        font = pygame.font.Font(font_path, font_size)
        title = font.render("AtomicGram", True, BLACK)
        title_rect = title.get_rect(center=(screen.get_width() //2, screen.get_height() // 2 - 165))
        screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(screen)

    def select_level(self):
        """
        Cambia la pantalla actual a la selección de nivel.
        """
        self.game.start_new_game()

    def quit_game(self):
        """
        Sale del juego.
        """
        pygame.quit()
        exit()

    def update(self):
        """
        Actualiza el estado del menú.
        """
        pass