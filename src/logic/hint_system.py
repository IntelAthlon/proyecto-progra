def get_hint(grid, row_clues, col_clues):
    """
    Proporciona una pista para el Nonogram, indicando una celda que debería ser llenada o vacía.

    Args:
        grid (list): La cuadrícula actual del Nonogram.
        row_clues (list): Pistas para las filas.
        col_clues (list): Pistas para las columnas.

    Returns:
        tuple: Una tupla (fila, columna, valor) indicando la celda y el valor correcto, o None si no hay pistas disponibles.
    """
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                if should_be_filled(grid, row, col, row_clues, col_clues):
                    return row, col, 1
                elif should_be_empty(grid, row, col, row_clues, col_clues):
                    return row, col, -1
    return None

def should_be_filled(grid, row, col, row_clues, col_clues):
    """
    Verifica si una celda debería ser llenada.

    Args:
        grid (list): La cuadrícula actual del Nonogram.
        row (int): Índice de la fila.
        col (int): Índice de la columna.
        row_clues (list): Pistas para las filas.
        col_clues (list): Pistas para las columnas.

    Returns:
        bool: True si la celda debería ser llenada, False en caso contrario.
    """
    row_filled = check_row(grid[row], row_clues[row])
    col_filled = check_col([grid[r][col] for r in range(len(grid))], col_clues[col])
    return row_filled and col_filled

def should_be_empty(grid, row, col, row_clues, col_clues):
    """
    Verifica si una celda debería estar vacía.

    Args:
        grid (list): La cuadrícula actual del Nonogram.
        row (int): Índice de la fila.
        col (int): Índice de la columna.
        row_clues (list): Pistas para las filas.
        col_clues (list): Pistas para las columnas.

    Returns:
        bool: True si la celda debería estar vacía, False en caso contrario.
    """
    row_empty = check_row(grid[row], row_clues[row], check_empty=True)
    col_empty = check_col([grid[r][col] for r in range(len(grid))], col_clues[col], check_empty=True)
    return row_empty or col_empty

def check_row(row, row_clue, check_empty=False):
    """
    Verifica si una fila cumple con las pistas dadas.

    Args:
        row (list): La fila a verificar.
        row_clue (list): Pistas para la fila.
        check_empty (bool, optional): Indica si se debe verificar si la fila está vacía. Por defecto es False.

    Returns:
        bool: True si la fila cumple con las pistas, False en caso contrario.
    """
    segments = get_segments(row)
    if check_empty:

        return not satisfies_clues(segments, row_clue)
    else:

        return satisfies_clues(segments, row_clue)

def check_col(col, col_clue, check_empty=False):
    """
    Verifica si una columna cumple con las pistas dadas.

    Args:
        col (list): La columna a verificar.
        col_clue (list): Pistas para la columna.
        check_empty (bool, optional): Indica si se debe verificar si la columna está vacía. Por defecto es False.

    Returns:
        bool: True si la columna cumple con las pistas, False en caso contrario.
    """
    segments = get_segments(col)
    if check_empty:
        return not satisfies_clues(segments, col_clue)
    else:
        return satisfies_clues(segments, col_clue)

def get_segments(line):
    """
    Obtiene los segmentos de una línea (fila o columna) del Nonogram.

    Args:
        line (list): La línea a analizar.

    Returns:
        list: Lista de segmentos encontrados en la línea.
    """
    segments = []
    count = 0
    for cell in line:
        if cell == 1:
            count += 1
        elif count > 0:
            segments.append(count)
            count = 0
    if count > 0:
        segments.append(count)
    return segments

def satisfies_clues(segments, clues):
    """
    Verifica si los segmentos encontrados cumplen con las pistas dadas.

    Args:
        segments (list): Lista de segmentos encontrados.
        clues (list): Pistas a verificar.

    Returns:
        bool: True si los segmentos cumplen con las pistas, False en caso contrario.
    """
    return segments == clues