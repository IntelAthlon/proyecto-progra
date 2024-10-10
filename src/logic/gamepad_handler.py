import pygame

class GamepadHandler:
    def __init__(self):
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            joystick.init()

    def get_input(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  # A button
                    return "select"
                elif event.button == 1:  # B button
                    return "cancel"
            elif event.type == pygame.JOYHATMOTION:
                if event.value[0] == 1:
                    return "right"
                elif event.value[0] == -1:
                    return "left"
                elif event.value[1] == 1:
                    return "up"
                elif event.value[1] == -1:
                    return "down"
        return None
