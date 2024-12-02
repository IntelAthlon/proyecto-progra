import time

import pygame.time


class Timer:
    def __init__(self):
        self.start_time = None
        self.total_time = 0
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.total_time = 0
            self.start_time = time.time()
            self.is_running = True

    def stop(self):
        if self.is_running:
            self.total_time += time.time() - self.start_time
            self.is_running = False

    def reset(self):
        self.start_time = None
        self.total_time = 0
        self.is_running = False

    def get_time(self):
        if self.is_running:
            return self.total_time + (time.time() - self.start_time)
        return self.total_time

    def set_time(self, last_time):
        self.total_time = last_time
        if self.is_running:
            self.start_time = time.time()