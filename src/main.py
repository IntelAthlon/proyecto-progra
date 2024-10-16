import pygame
import sys
import os
from game import Game
from src.ui.level_select_screen import LevelSelectScreen
from src.ui.menu import Menu
from src.ui.game_screen import GameScreen
from src.ui.editor_screen import EditorScreen


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("AtomicGram 1.0")
    clock = pygame.time.Clock()

    game = Game(screen)
    #game.run()
    menu = Menu(game)
    game_screen = GameScreen(game)
    editor_screen = EditorScreen(game)
    level_select_screen = LevelSelectScreen(game)

    screens = {
        "menu": menu,
        "game": game_screen,
        "editor": editor_screen,
        "level_select": level_select_screen

    }

    while True:
        current_screen = screens[game.current_screen]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            current_screen.handle_event(event)

        current_screen.update()
        screen.fill((255, 255, 255))
        current_screen.draw(screen)
        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()