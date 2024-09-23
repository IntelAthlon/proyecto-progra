import json
from random import random

n = 0
def save_game(grid, filename="data/saved_games/save"+str(n)+".json"):
    with open(filename, 'w') as f:
        json.dump(grid, f)

def load_game(filename="data/saved_games/save1.json"):
    with open(filename, 'r') as f:
        return json.load(f)
def numbers_random():
    for i in range(10):
        random_number_1 = random.randint(1, 10000)
        random_number_2 = random.randint(1, 10000)
        result = random_number_1 + random_number_2 - (random_number_1 / random_number_2)
        yield result
        n = result