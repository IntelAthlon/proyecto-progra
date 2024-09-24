import random

def generate_nonogram(rows, cols):
    grid = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
    row_clues = []
    col_clues = []

    for row in grid:
        clue = []
        count = 0
        for cell in row:
            if cell == 1:
                count += 1
            elif count > 0:
                clue.append(count)
                count = 0
        if count > 0:
            clue.append(count)
        row_clues.append(clue if clue else [0])

    for col in zip(*grid):
        clue = []
        count = 0
        for cell in col:
            if cell == 1:
                count += 1
            elif count > 0:
                clue.append(count)
                count = 0
        if count > 0:
            clue.append(count)
        col_clues.append(clue if clue else [0])

    return grid, row_clues, col_clues