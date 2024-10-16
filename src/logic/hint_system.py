def get_hint(grid, row_clues, col_clues):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                if should_be_filled(grid, row, col, row_clues, col_clues):
                    return row, col, 1
                elif should_be_empty(grid, row, col, row_clues, col_clues):
                    return row, col, -1
    return None

def should_be_filled(grid, row, col, row_clues, col_clues):
    row_filled = check_row(grid[row], row_clues[row])
    col_filled = check_col([grid[r][col] for r in range(len(grid))], col_clues[col])
    return row_filled and col_filled

def should_be_empty(grid, row, col, row_clues, col_clues):
    row_empty = check_row(grid[row], row_clues[row], check_empty=True)
    col_empty = check_col([grid[r][col] for r in range(len(grid))], col_clues[col], check_empty=True)
    return row_empty or col_empty

def check_row(row, row_clue, check_empty=False):
    segments = get_segments(row)
    if check_empty:

        return not satisfies_clues(segments, row_clue)
    else:

        return satisfies_clues(segments, row_clue)

def check_col(col, col_clue, check_empty=False):
    segments = get_segments(col)
    if check_empty:
        return not satisfies_clues(segments, col_clue)
    else:
        return satisfies_clues(segments, col_clue)

def get_segments(line):
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
    return segments == clues