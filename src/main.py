import pygame
import sys
import os
from src.Game import Game
from src.ui.LevelSelectScreen import LevelSelectScreen
from src.ui.Menu import Menu
from src.ui.GameScreen import GameScreen

def main():
    """
        Función principal que inicializa y ejecuta el juego AtomicGram.

    Atributos e Instancias:
    main(): Función principal que inicializa Pygame, configura la ventana del juego, carga la imagen de fondo, y gestiona el bucle principal del juego.
    WINDOW_WIDTH y WINDOW_HEIGHT: Dimensiones de la ventana del juego.
    screen: Superficie de la pantalla donde se dibuja el juego.
    clock: Objeto para controlar el tiempo y la velocidad de fotogramas.
    background_image: Imagen de fondo del juego.
    game: Instancia de la clase Game.
    menu, game_screen, editor_screen, level_select_screen: Instancias de las diferentes pantallas del juego.
    screens: Diccionario que mapea los nombres de las pantallas a sus respectivas instancias.
    joystick_connected: Booleano que indica si hay un joystick conectado.
    mouse_speed: Velocidad del cursor del ratón.
    console_controller_x, console_controller_y: Coordenadas del cursor del ratón controlado por el joystick.
        """
    joystick = None
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 900
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AtomicGram 1.0")
    clock = pygame.time.Clock()

    background_image = pygame.image.load(os.path.join("assets", "images", "background.jpg"))
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    joystick_connected = False
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        joystick_connected = True
    mouse_speed = 5
    console_controller_x, console_controller_y = pygame.mouse.get_pos()
    game = Game(screen, joystick)
    #game.run()
    menu = Menu(game)
    game_screen = GameScreen(game)
    level_select_screen = LevelSelectScreen(game)

    screens = {
        "menu": menu,
        "game": game_screen,
        "level_select": level_select_screen

    }

    while True:
        current_screen = screens[game.current_screen]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if joystick_connected and event.type == pygame.JOYAXISMOTION:
                # Derecha o izquierda
                x_axis = joystick.get_axis(0)
                # Arriba o abajo
                y_axis = joystick.get_axis(1)

                console_controller_x += x_axis * mouse_speed
                console_controller_y += y_axis * mouse_speed
                mouse_x = max(0, min(console_controller_x, WINDOW_WIDTH))
                mouse_y = max(0, min(console_controller_y, WINDOW_WIDTH))
                pygame.mouse.set_pos(mouse_x, mouse_y)
            current_screen.handle_event(event)

        current_screen.update()
        screen.blit(background_image, (0, 0))
        current_screen.draw(screen)
        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()