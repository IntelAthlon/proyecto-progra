import pygame.mixer

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "select": pygame.mixer.Sound("C:/Users/carlo/Desktop/proyecto progra/proyecto-progra/assets/sounds/select.mp3"),
            "cancel": pygame.mixer.Sound("C:/Users/carlo/Desktop/proyecto progra/proyecto-progra/assets/sounds/cancel.mp3"),
            "complete": pygame.mixer.Sound("C:/Users/carlo/Desktop/proyecto progra/proyecto-progra/assets/sounds/complete.mp3")
        }
        self.music = pygame.mixer.Sound("C:/Users/carlo/Desktop/proyecto progra/proyecto-progra/assets/sounds/back.mp3")

    def play_sound(self, sound_name):
        self.sounds[sound_name].play()

    def play_music(self):
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    def stop_music(self):
        pygame.mixer.music.stop()