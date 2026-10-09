'''
puzzle_generator.py
Random Sudoku puzzle generation with a guaranteed unique solution.
The generator first builds a complete, valid grid using randomized
backtracking, then removes digits one by one. A digit is only kept
removed when the puzzle still admits exactly one solution, which is
verified with a solution-counting backtracking search.
'''
import random
from sudoku_board import GRID_SIZE, BOX_SIZE, EMPTY
def _find_empty(grid):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == EMPTY:
                return r, c
    return None
def _is_safe(grid, row, col, value):
    # row/col
    for i in range(GRID_SIZE):
        if grid[row][i] == value or grid[i][col] == value:
            return False
    br, bc = (row // BOX_SIZE) * BOX_SIZE, (col // BOX_SIZE) * BOX_SIZE
    for r in range(br, br + BOX_SIZE):
        for c in range(bc, bc + BOX_SIZE):
            if grid[r][c] == value:
                return False
    return True
def _count_solutions(grid, limit=2):
    """Count solutions up to `limit` using backtracking."""
    count = 0
    empty = _find_empty(grid)
    if empty is None:
        return 1
    row, col = empty
    for value in range(1, GRID_SIZE + 1):
        if _is_safe(grid, row, col, value):
            grid[row][col] = value
            count += _count_solutions(grid, limit)
            grid[row][col] = EMPTY
            if count >= limit:
                break
    return count
def _fill_grid(grid):
    """Fill an empty grid completely with a random valid solution."""
    empty = _find_empty(grid)
    if empty is None:
        return True
    row, col = empty
    values = list(range(1, GRID_SIZE + 1))
    random.shuffle(values)
    for value in values:
        if _is_safe(grid, row, col, value):
            grid[row][col] = value
            if _fill_grid(grid):
                return True
            grid[row][col] = EMPTY
    return False
class PuzzleGenerator:
    DIFFICULTY_REMOVALS = {
        "easy": 45,
        "medium": 51,
        "hard": 55,
    }
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    def generate(self, difficulty="medium"):
        """Return (puzzle, solution) as 9x9 nested lists (0 = empty)."""
        removals = self.DIFFICULTY_REMOVALS.get(difficulty, self.DIFFICULTY_REMOVALS["medium"])
        solution = [[EMPTY]*GRID_SIZE for _ in range(GRID_SIZE)]
        _fill_grid(solution)
        puzzle = [row[:] for row in solution]
        removed = 0
        cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
        self.rng.shuffle(cells)
        for r, c in cells:
            if removed >= removals:
                break
            backup = puzzle[r][c]
            puzzle[r][c] = EMPTY
            if _count_solutions([row[:] for row in puzzle], limit=2) == 1:
                removed += 1
            else:
                puzzle[r][c] = backup
        return puzzle, solution