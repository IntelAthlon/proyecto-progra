
def solve_nonogram(row_clues, col_clues):
    rows = len(row_clues)
    cols = len(col_clues)
    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def is_valid(grid):
        for r, clue in enumerate(row_clues):
            if get_clue(grid[r]) != clue:
                return False
        for c in range(cols):
            if get_clue([grid[r][c] for r in range(rows)]) != col_clues[c]:
                return False
        return True

    def get_clue(line):
        clue = []
        count = 0
        for cell in line:
            if cell == 1:
                count += 1
            elif count > 0:
                clue.append(count)
                count = 0
        if count > 0:
            clue.append(count)
        return clue if clue else [0]

    def backtrack(r, c):
        if r == rows:
            return is_valid(grid)
        if c == cols:
            return backtrack(r + 1, 0)

        for value in [0, 1]:
            grid[r][c] = value
            if backtrack(r, c + 1):
                return True
        grid[r][c] = 0
        return False

    backtrack(0, 0)
    return grid

#def is_solvable(grid, row_clues, col_clues):
 #   solved_grid = solve_nonogram(row_clues, col_clues)
  #  return solved_grid == grid