import pygame


class ProgressDisplay:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 24)

    def draw_category_progress(self, screen, x, y, width, height):
        for i, category in enumerate(self.game.categories):
            completed, total = self.game.progress_tracker.get_category_progress(category)
            progress_text = f"{category}: {completed}/{total}"
            text_surface = self.font.render(progress_text, True, (0, 0, 0))
            screen.blit(text_surface, (x, y + i * 30))

            progress_width = int((completed / total) * width)
            pygame.draw.rect(screen, (200, 200, 200), (x, y + i * 30 + 25, width, 20))
            pygame.draw.rect(screen, (0, 255, 0), (x, y + i * 30 + 25, progress_width, 20))

    def draw_level_progress(self, screen, category, x, y, width, height):
        levels = self.game.categories[category]
        for i, level in enumerate(levels):
            is_complete = self.game.progress_tracker.is_level_complete(category, level['name'])
            color = (0, 255, 0) if is_complete else (200, 200, 200)
            pygame.draw.rect(screen, color, (x + (i % 5) * 50, y + (i // 5) * 50, 40, 40))

            level_text = self.font.render(str(i + 1), True, (0, 0, 0))
            screen.blit(level_text, (x + (i % 5) * 50 + 15, y + (i // 5) * 50 + 10))