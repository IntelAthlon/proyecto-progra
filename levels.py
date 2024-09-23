import random

def generate_random_nonogram(grid_size):
    return [[random.randint(0, 1) for _ in range(grid_size)] for _ in range(grid_size)]

def generate_levels():
    levels = []
    sizes = [8, 10, 15, 20, 25]
    for _ in range(50):
        size = random.choice(sizes)
        levels.append(generate_random_nonogram(size))
    return levels
