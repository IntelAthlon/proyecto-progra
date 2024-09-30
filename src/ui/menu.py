import json
import os
from random import random
from types import NoneType
from tkinter import filedialog
import tkinter as tk
from PIL.ImageChops import screen
from src.ui.components import Button
from src.utils.image_converter import image_to_nonogram
from src import ui_p

import pygame
from src.ui.components import Button

class Menu:
    def __init__(self, game):
        self.game = game
        self.buttons = [
            Button("Select Level", 300, 200, 200, 50, self.select_level),
            Button("Load Game", 300, 260, 200, 50, self.load_game),
            Button("Editor", 300, 320, 200, 50, self.start_editor),
            Button("Quit", 300, 380, 200, 50, self.quit_game)
        ]

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 48)
        title = font.render("AtomicGram", True, (0, 0, 0))
        screen.blit(title, (300, 100))

        for button in self.buttons:
            button.draw(screen)

    def select_level(self):
        self.game.start_new_game()

    def load_game(self):
        self.game.load_game()

    def start_editor(self):
        self.game.start_editor()

    def quit_game(self):
        pygame.quit()
        quit()