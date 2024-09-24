import itertools

from PIL import Image
import numpy as np


def image_to_nonogram(image_path, size):
    image = Image.open(image_path).convert('L')
    image = image.resize((size, size), Image.ANTIALIAS)
    image_array = np.array(image)
    threshold = 128
    nonogram = (image_array < threshold).astype(int)

    row_clues = []
    col_clues = []

    for row in nonogram:
        clue = [len(list(group)) for key, group in itertools.groupby(row) if key == 1]
        row_clues.append(clue if clue else [0])

    for col in nonogram.T:
        clue = [len(list(group)) for key, group in itertools.groupby(col) if key == 1]
        col_clues.append(clue if clue else [0])

    return nonogram.tolist(), row_clues, col_clues