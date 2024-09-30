import random


def generate_nonogram(rows, cols, difficulty):
    # Ajustar la densidad según la dificultad
    if difficulty == 'easy':
        density = 0.6
    elif difficulty == 'medium':
        density = 0.5
    else:  # hard
        density = 0.4

    # Generar la cuadrícula
    grid = [[1 if random.random() < density else 0 for _ in range(cols)] for _ in range(rows)]

    # Generar las pistas
    row_clues = [get_clues(row) for row in grid]
    col_clues = [get_clues([grid[r][c] for r in range(rows)]) for c in range(cols)]

    return {
        'grid': grid,
        'row_clues': row_clues,
        'col_clues': col_clues
    }

def get_clues(line):
    clues = []
    count = 0
    for cell in line:
        if cell == 1:
            count += 1
        elif count > 0:
            clues.append(count)
            count = 0
    if count > 0:
        clues.append(count)
    return clues if clues else [0]

