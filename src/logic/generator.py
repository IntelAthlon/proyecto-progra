import random


def generate_nonogram(rows, cols, difficulty):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    fill_ratio = 0.3 + (difficulty * 0.1)  # Adjust fill ratio based on difficulty
    for r in range(rows):
        for c in range(cols):
            if random.random() < fill_ratio:
                grid[r][c] = 1
    return grid


