from PIL import Image
import numpy as np

def image_to_nonogram(image_path, grid_size):
    image = Image.open(image_path).convert('L')
    image = image.resize((grid_size, grid_size), Image.ANTIALIAS)
    image_array = np.array(image)
    threshold = 128
    nonogram = (image_array < threshold).astype(int)
    return nonogram.tolist()
