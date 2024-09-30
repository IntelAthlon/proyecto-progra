class Tutorial:
    def __init__(self, game):
        self.game = game
        self.steps = [
            "Bienvenido a AtomicGram. En este juego, debes rellenar celdas para formar una imagen.",
            "Los números en los lados indican cuántas celdas consecutivas deben rellenarse en cada fila o columna.",
            "Haz clic izquierdo para rellenar una celda, y clic derecho para marcarla con una X.",
            "¡Vamos a intentarlo! Rellena la primera fila según el número indicado.",
            "¡Bien hecho! Ahora intenta resolver la primera columna.",
            "Excelente. Continúa resolviendo el resto del puzzle.",
            "¡Felicidades! Has completado el tutorial. ¡Disfruta jugando Nonogramas!"
        ]
        self.current_step = 0

    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
        else:
            self.game.end_tutorial()

    def draw(self, screen):
        text_surface = self.game.font.render(self.steps[self.current_step], True, (0, 0, 0))
        screen.blit(text_surface, (50, 50))