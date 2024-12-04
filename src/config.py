# Configuración de la ventana del juego
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 750
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Niveles de dificultad del juego (esto es una beta, no es seguro que se use más adelante)
DIFFICULTY_EASY = 0
DIFFICULTY_MEDIUM = 1
DIFFICULTY_HARD = 2

# Configuración de la cuadrícula para la pantalla del juego
MIN_GRID_SIZE = 5
MAX_GRID_SIZE = 100
DEFAULT_GRID_SIZE = 15

# Rutas de guardado
SAVE_GAME_PATH = "saved_games/"
CUSTOM_NONOGRAMS_PATH = "user_created/"

# Configuración de la interfaz de usuario
CELL_SIZE = 30
GRID_OFFSET = (100, 100)
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

class Settings:
    """
    Clase que representa la configuración del juego.

    Atributos:
        color_theme (str): Tema de color actual.
        grid_size (str): Tamaño de la cuadrícula.
        sound_volume (float): Volumen del sonido.
        music_volume (float): Volumen de la música.
    """

    def __init__(self):
        """
        Inicializa una instancia de la clase Settings con valores predeterminados.
        """
        self.color_theme = "default"
        self.grid_size = "medium"
        self.sound_volume = 0.7
        self.music_volume = 0.5

    def change_color_theme(self, theme):
        """
        Cambia el tema de color del juego.

        Args:
            theme (str): Nuevo tema de color.
        """
        self.color_theme = theme

    def change_grid_size(self, size):
        """
        Cambia el tamaño de la cuadrícula del juego.

        Args:
            size (str): Nuevo tamaño de la cuadrícula.
        """
        self.grid_size = size

    def change_sound_volume(self, volume):
        """
        Cambia el volumen del sonido del juego.

        Args:
            volume (float): Nuevo volumen del sonido.
        """
        self.sound_volume = volume

    def change_music_volume(self, volume):
        """
        Cambia el volumen de la música del juego.

        Args:
            volume (float): Nuevo volumen de la música.
        """
        self.music_volume = volume