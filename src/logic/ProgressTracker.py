import json
import os

class ProgressTracker:
    """
    Clase que rastrea el progreso del jugador en el juego.

    Atributos:
        progress_file (str): Ruta al archivo de progreso del jugador.
        progress (dict): Diccionario que contiene el progreso del jugador.
    """
    def __init__(self, progress_file="data/player_progress.json"):
        """
        Inicializa una instancia de la clase ProgressTracker.

        Args:
            progress_file (str, optional): Ruta al archivo de progreso del jugador. Por defecto es "data/player_progress.json".
        """
        self.progress_file = progress_file
        self.progress = self.load_progress()

    def load_progress(self):
        """
        Carga el progreso del jugador desde un archivo JSON.

        Returns:
            dict: Diccionario que contiene el progreso del jugador.
        """

        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {}

    def save_progress(self):
        """
        Guarda el progreso del jugador en un archivo JSON.
        """
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f)

    def mark_level_complete(self, category, level_name):
        """
        Marca un nivel como completado.

        Args:
            category (str): Categoría del nivel (por ejemplo, "easy", "medium", "hard").
            level_name (str): Nombre del nivel.
        """
        if category not in self.progress:
            self.progress[category] = {}
        self.progress[category][level_name] = True
        self.save_progress()

    def is_level_complete(self, category, level_name):
        """
        Verifica si un nivel está completado.

        Args:
            category (str): Categoría del nivel.
            level_name (str): Nombre del nivel.

        Returns:
            bool: True si el nivel está completado, False en caso contrario.
        """
        return self.progress.get(category, {}).get(level_name, False)

    def get_category_progress(self, category):
        """
        Obtiene el progreso en una categoría específica.

        Args:
            category (str): Categoría del nivel.

        Returns:
            int: Número de niveles completados en la categoría.
        """
        category_progress = self.progress.get(category, {})
        return len(category_progress)
