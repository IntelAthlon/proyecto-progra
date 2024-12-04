import itertools
from PIL import Image
import numpy as np
from pygame.examples.cursors import image

def image_to_nonogram(image_path, size = 20, num_colors=2):
    """
    Convierte una imagen en un Nonograma.

    Args:
        image_path (str): Ruta a la imagen a convertir.
        size (int, optional): Tamaño de la cuadrícula del Nonogram. Por defecto es 20.
        num_colors (int, optional): Número de colores para la cuantización de la imagen. Por defecto es 2 (blanco y negro).

    Returns:
        list: Una lista que contiene la cuadrícula del Nonogram, las pistas de las filas y las pistas de las columnas.
    """
    image = Image.open(image_path)
    img_alpha = False
    if image.has_transparency_data:
        img_alpha = True
    image = Image.open(image_path).convert('L')
    pixels = image.getdata()
    black_thresh = 50
    nblack = 0
    for pixel in pixels:
        if pixel < black_thresh:
            nblack += 1
    n = len(pixels)

    image = Image.open(image_path).convert('RGB')
    image = image.resize((size, size), Image.Resampling.LANCZOS)

    image_quantized = image.convert('P', palette=Image.ADAPTIVE, colors=num_colors)
    image_quantized = np.array(image_quantized)

    if (nblack / float(n)) > 0.5 or img_alpha:
        image_quantized = np.logical_not(image_quantized).astype(int)


    row_clues = []
    col_clues = []

    for row in image_quantized:
        clues = []
        current_color = None
        count = 0
        for pixel in row:
            if pixel != current_color:
                if current_color==1:
                    clues.append(count)
                current_color = pixel
                count = 1
            else:
                count += 1
        if current_color==1:
            clues.append(count)
        row_clues.append(clues if clues else [0])

    for col in image_quantized.T:
        clues = []
        current_color = None
        count = 0
        for pixel in col:
            if pixel != current_color:
                if current_color==1:
                    clues.append(count)
                current_color = pixel
                count = 1
            else:
                count += 1
        if current_color==1:
            clues.append(count)
        col_clues.append(clues if clues else [0])

    return [image_quantized.tolist(), row_clues, col_clues]

