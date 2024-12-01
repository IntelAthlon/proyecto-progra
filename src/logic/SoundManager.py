import pygame
import pygame.mixer

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "select": pygame.mixer.Sound("assets/sounds/select.mp3"),
            "cancel": pygame.mixer.Sound("assets/sounds/cancel.mp3"),
            "complete": pygame.mixer.Sound("assets/sounds/complete.mp3")
        }
        self.music = pygame.mixer.Sound("assets/sounds/back.mp3")

    def play_sound(self, sound_name):
        self.sounds[sound_name].play()

    def play_music(self):
        pygame.mixer.music.load("assets/sounds/back.mp3")
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def resume_music(self):
        pygame.mixer.music.unpause()