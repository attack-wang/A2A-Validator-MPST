'''
sudoku_generator.py
Generates Sudoku puzzles with unique solutions at three difficulty levels.
'''
import random
DIFFICULTY_HOLES = {"easy": 40, "medium": 48, "hard": 54}
def _find_empty(grid):
    """Return the (row, col) of the first empty cell, or None if full."""
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None
def _is_valid_placement(grid, row, col, value):
    """Check whether value can legally be placed at (row, col) on grid."""
    for c in range(9):
        if grid[row][c] == value:
            return False
    for r in range(9):
        if grid[r][col] == value:
            return False
    br, bc = (row // 3) * 3, (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if grid[r][c] == value:
                return False
    return True
def _fill_grid(grid):
    """Fill an empty grid completely using randomized backtracking."""
    empty = _find_empty(grid)
    if empty is None:
        return True
    row, col = empty
    digits = list(range(1, 10))
    random.shuffle(digits)
    for value in digits:
        if _is_valid_placement(grid, row, col, value):
            grid[row][col] = value
            if _fill_grid(grid):
                return True
            grid[row][col] = 0
    return False
def count_solutions(grid, limit=2):
    """Count solutions of the grid (0 = empty), stopping once `limit` found."""
    empty = _find_empty(grid)
    if empty is None:
        return 1
    row, col = empty
    total = 0
    for value in range(1, 10):
        if _is_valid_placement(grid, row, col, value):
            grid[row][col] = value
            total += count_solutions(grid, limit - total)
            grid[row][col] = 0
            if total >= limit:
                break
    return total
class SudokuGenerator:
    """Generates full grids and puzzles with unique solutions."""
    @staticmethod
    def generate_full_grid():
        """Return a randomly generated, complete, valid 9x9 Sudoku grid."""
        grid = [[0] * 9 for _ in range(9)]
        if not _fill_grid(grid):
            raise RuntimeError("Failed to generate a complete Sudoku grid.")
        return grid
    @staticmethod
    def generate_puzzle(difficulty="medium"):
        """Return (puzzle, solution) with a unique solution; difficulty in
        {'easy', 'medium', 'hard'} controls how many clues are removed."""
        difficulty = difficulty.lower()
        if difficulty not in DIFFICULTY_HOLES:
            difficulty = "medium"
        solution = SudokuGenerator.generate_full_grid()
        puzzle = [row[:] for row in solution]
        target_holes = DIFFICULTY_HOLES[difficulty]
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        removed = 0
        for row, col in cells:
            if removed >= target_holes:
                break
            backup = puzzle[row][col]
            puzzle[row][col] = 0
            test_grid = [r[:] for r in puzzle]
            if count_solutions(test_grid, limit=2) == 1:
                removed += 1
            else:
                puzzle[row][col] = backup
        return puzzle, solution