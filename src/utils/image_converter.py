import itertools
from PIL import Image
import numpy as np


def image_to_nonogram(image_path, size = 100, num_colors=2):
    image = Image.open(image_path).convert('RGB')
    image = image.resize((size, size), Image.Resampling.LANCZOS)
    image_array = np.array(image)

    image_quantized = image.convert('P', palette=Image.ADAPTIVE, colors=num_colors)
    image_quantized = np.array(image_quantized)

    row_clues = []
    col_clues = []

    for row in image_quantized:
        clues = []
        current_color = None
        count = 0
        for pixel in row:
            if pixel != current_color:
                if current_color is not None:
                    clues.append((current_color, count))
                current_color = pixel
                count = 1
            else:
                count += 1
        if current_color is not None:
            clues.append((current_color, count))
        row_clues.append(clues if clues else [(0, 0)])

    for col in image_quantized.T:
        clues = []
        current_color = None
        count = 0
        for pixel in col:
            if pixel != current_color:
                if current_color is not None:
                    clues.append((current_color, count))
                current_color = pixel
                count = 1
            else:
                count += 1
        if current_color is not None:
            clues.append((current_color, count))
        col_clues.append(clues if clues else [(0, 0)])

    return image_quantized.tolist(), row_clues, col_clues
