import pygame
from src.config import *

class Button:
    def __init__(self, text, x, y, width, height, callback, sound_manager=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.sound_manager = sound_manager

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.sound_manager:
                    self.sound_manager.play_sound("select")
                self.callback()