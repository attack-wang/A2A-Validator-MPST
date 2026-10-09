'''
sudoku_generator.py
Generates Sudoku puzzles and their solutions for a requested difficulty.
Fixes: (1) defines the previously missing SudokuGenerator class that caused
the ImportError, (2) implements the previously undefined _is_valid helper,
(3) provides the public API (DIFFICULTY_LEVELS, __init__, generate) that
sudoku_gui.py depends on.
'''
import random
class SudokuGenerator:
    """Generates a unique-solution Sudoku puzzle at a given difficulty."""
    DIFFICULTY_LEVELS = {
        'easy': 40,    # number of clues to keep
        'medium': 32,
        'hard': 26,
    }
    def __init__(self, difficulty='medium'):
        if difficulty not in self.DIFFICULTY_LEVELS:
            difficulty = 'medium'
        self.difficulty = difficulty
        self.target_clues = self.DIFFICULTY_LEVELS[difficulty]
    # ----- public API -----
    def generate(self):
        """Return (puzzle, solution) as two 9x9 lists of ints (0 = empty)."""
        solution = self._make_full_grid()
        puzzle = [row[:] for row in solution]
        self._dig_holes(puzzle)
        return puzzle, solution
    # ----- grid construction -----
    def _make_full_grid(self):
        grid = [[0] * 9 for _ in range(9)]
        self._fill_grid(grid)
        return grid
    def _fill_grid(self, grid):
        """Backtracking fill of the whole grid with a randomized valid solution."""
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    values = list(range(1, 10))
                    random.shuffle(values)
                    for value in values:
                        if self._is_valid(grid, r, c, value):
                            grid[r][c] = value
                            if self._fill_grid(grid):
                                return True
                            grid[r][c] = 0
                    return False
        return True
    def _dig_holes(self, puzzle):
        """Remove clues while guaranteeing the puzzle keeps a unique solution."""
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        clues = 81
        for r, c in cells:
            if clues <= self.target_clues:
                break
            removed = puzzle[r][c]
            if removed == 0:
                continue
            puzzle[r][c] = 0
            test = [row[:] for row in puzzle]
            if self._count_solutions(test, 2) != 1:
                puzzle[r][c] = removed  # restore: removal broke uniqueness
            else:
                clues -= 1
    # ----- solver helpers -----
    def _is_valid(self, grid, row, col, value):
        """True if `value` can be placed at (row, col) without conflicts."""
        if any(grid[row][c] == value for c in range(9) if c != col):
            return False
        if any(grid[r][col] == value for r in range(9) if r != row):
            return False
        br, bc = 3 * (row // 3), 3 * (col // 3)
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if (r, c) != (row, col) and grid[r][c] == value:
                    return False
        return True
    def _count_solutions(self, grid, limit):
        """Count solutions up to `limit`, with early termination."""
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    total = 0
                    for value in range(1, 10):
                        if self._is_valid(grid, r, c, value):
                            grid[r][c] = value
                            total += self._count_solutions(grid, limit - total)
                            grid[r][c] = 0
                            if total >= limit:
                                return total
                    return total
        return 1