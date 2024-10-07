import os

import pygame
import json
from src.ui.components import Button
from src.config import *
from src.nonogram import Nonogram

class GameScreen:
    def __init__(self, game):
        self.game = game
        self.nonogram = None
        self.buttons = [
            Button("Hint", 650, 100, BUTTON_WIDTH, BUTTON_HEIGHT, self.get_hint),
            Button("Undo", 650, 160, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.undo),
            Button("Redo", 650, 220, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.redo),
            Button("Save", 650, 280, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.save_game),
            Button("Menu", 650, 340, BUTTON_WIDTH, BUTTON_HEIGHT, self.return_to_menu)
        ]
        self.load_player_progress()

    def load_player_progress(self):
        try:
            with open("data/player_progress.json", "r") as f:
                self.player_progress = json.load(f)
        except FileNotFoundError:
            self.player_progress = {
                "easy": {},
                "medium": {},
                "hard": {}
            }

    def save_player_progress(self):
        with open("data/player_progress.json", "w") as f:
            json.dump(self.player_progress, f, indent=2)

