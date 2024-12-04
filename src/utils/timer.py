import time
import pygame.time

class Timer:
    """
    Clase que representa un temporizador para el juego.

    Atributos:
        start_time (float): Tiempo de inicio del temporizador.
        total_time (float): Tiempo total acumulado.
        is_running (bool): Indica si el temporizador está en funcionamiento.
    """

    def __init__(self):
        """
        Inicializa una instancia de la clase Timer.
        """
        self.start_time = None
        self.total_time = 0
        self.is_running = False

    def start(self):
        """
        Inicia el temporizador.
        """
        if not self.is_running:
            self.total_time = 0
            self.start_time = time.time()
            self.is_running = True

    def stop(self):
        """
        Detiene el temporizador y acumula el tiempo transcurrido.
        """
        if self.is_running:
            self.total_time += time.time() - self.start_time
            self.is_running = False

    def reset(self):
        """
        Reinicia el temporizador.
        """
        self.start_time = None
        self.total_time = 0
        self.is_running = False

    def get_time(self):
        """
        Obtiene el tiempo transcurrido del temporizador.

        Returns:
            float: Tiempo total transcurrido.
        """
        if self.is_running:
            return self.total_time + (time.time() - self.start_time)
        return self.total_time

    def set_time(self, last_time):
        """
        Establece el tiempo del temporizador.

        Args:
            last_time (float): Tiempo a establecer en el temporizador.
        """
        self.total_time = last_time
        if self.is_running:
            self.start_time = time.time()