import itertools
import json
import os



def save_game(nonogram, filename):
    data = {
        'grid': nonogram.grid,
        'row_clues': nonogram.row_clues,
        'col_clues': nonogram.col_clues,
        'timer': nonogram.timer
    }
    with open(filename, 'w') as f:
        json.dump(data, f)


def load_games(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def save_custom_nonogram(grid, filename):
    row_clues = []
    col_clues = []

    for row in grid:
        clue = [len(list(group)) for key, group in itertools.groupby(row) if key == 1]
        row_clues.append(clue if clue else [0])

    for col in zip(*grid):
        clue = [len(list(group)) for key, group in itertools.groupby(col) if key == 1]
        col_clues.append(clue if clue else [0])

    data = {
        'grid': grid,
        'row_clues': row_clues,
        'col_clues': col_clues
    }

    with open(filename, 'w') as f:
        json.dump(data, f)


def load_custom_nonogram(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    if isinstance(data, dict) and 'grid' in data and 'row_clues' in data and 'col_clues' in data:
        return data['grid'], data['row_clues'], data['col_clues']
    else:
        raise ValueError(f"Incorrect JSON structure in file: {filename}")

def get_saved_games():
    saved_games = []
    for filename in os.listdir('data/saved_games'):
        if filename.endswith('.json'):
            saved_games.append(filename)
    return saved_games


def get_custom_nonograms():
    custom_nonograms = []
    for filename in os.listdir('data/user_created'):
        if filename.endswith('.json'):
            custom_nonograms.append(filename)
    return custom_nonograms