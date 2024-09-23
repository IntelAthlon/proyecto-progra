import json

def save_game(state, filename):
    with open(filename, 'w') as f:
        json.dump(state, f)

def load_game(filename):
    with open(filename, 'r') as f:
        return json.load(f)