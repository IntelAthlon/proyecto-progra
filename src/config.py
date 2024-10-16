#game setting window display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#game difficulty levels (this is a beta, is not sure that we use this a few later)
DIFFICULTY_EASY = 0
DIFFICULTY_MEDIUM = 1
DIFFICULTY_HARD = 2

#Grid settings for the game screen
MIN_GRID_SIZE = 5
MAX_GRID_SIZE = 100
DEFAULT_GRID_SIZE = 15


SAVE_GAME_PATH = "saved_games/"
CUSTOM_NONOGRAMS_PATH = "user_created/"

#UI settings
CELL_SIZE = 30
GRID_OFFSET = (100, 100)
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

class Settings:
    def __init__(self):
        self.color_theme = "default"
        self.grid_size = "medium"
        self.sound_volume = 0.7
        self.music_volume = 0.5

    def change_color_theme(self, theme):
        self.color_theme = theme

    def change_grid_size(self, size):
        self.grid_size = size

    def change_sound_volume(self, volume):
        self.sound_volume = volume

    def change_music_volume(self, volume):
        self.music_volume = volume