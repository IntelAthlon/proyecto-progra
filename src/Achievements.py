class Achievement:
    def __init__(self, name, description, condition):
        self.name = name
        self.description = description
        self.condition = condition
        self.unlocked = False

    def check(self, game):
        if not self.unlocked and self.condition(game):
            self.unlocked = True
            print(f"¡Logro desbloqueado: {self.name}!")
            print(self.description)

class AchievementSystem:
    def __init__(self):
        self.achievements = [
            Achievement("Principiante", "Completa tu primer nonograma", lambda game: game.completed_puzzles >= 1),
            Achievement("Aficionado", "Completa 10 nonogramas", lambda game: game.completed_puzzles >= 10),
            Achievement("Maestro", "Completa 50 nonogramas", lambda game: game.completed_puzzles >= 50),
            Achievement("Velocista", "Completa un nonograma en menos de 1 minuto", lambda game: game.fastest_time < 60),
            Achievement("Creativo", "Crea tu primer nonograma personalizado", lambda game: game.created_puzzles >= 1),
        ]

    def update(self, game):
        for achievement in self.achievements:
            achievement.check(game)

    def get_unlocked(self):
        return [ach for ach in self.achievements if ach.unlocked]

    def get_locked(self):
        return [ach for ach in self.achievements if not ach.unlocked]