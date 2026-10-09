'''
puzzle_generator.py
Generates new Sudoku puzzles with a guaranteed unique solution.
A complete, valid grid is produced via randomized backtracking, then
cells are removed one by one (in random order). After each removal the
SudokuSolver is used to confirm the puzzle still has exactly one
solution; if not, the cell is restored. Difficulty controls how many
cells are removed.
'''
import random
from sudokusolver import SudokuSolver
class PuzzleGenerator:
    """Creates random, uniquely solvable Sudoku puzzles at three difficulties."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    REMOVAL_TARGETS = {
        "easy": 40,     # ~41 givens
        "medium": 50,   # ~31 givens
        "hard": 56,     # ~25 givens
    }
    def __init__(self, seed=None):
        """Optionally seed the RNG for reproducible puzzles (mainly for tests)."""
        self.rng = random.Random(seed)
        self.solver = SudokuSolver()
    def generate_puzzle(self, difficulty=MEDIUM):
        """Generate a puzzle; returns (puzzle, solution) as 9x9 lists of lists."""
        if difficulty not in self.REMOVAL_TARGETS:
            raise ValueError("Difficulty must be 'easy', 'medium' or 'hard'.")
        solution = self.generate_full_grid()
        puzzle = [row[:] for row in solution]
        self._remove_cells(puzzle, self.REMOVAL_TARGETS[difficulty])
        return puzzle, solution
    def generate_full_grid(self):
        """Create a fully solved 9x9 grid using randomized backtracking."""
        grid = [[0] * 9 for _ in range(9)]
        self._fill_grid(grid)
        return grid
    def _fill_grid(self, grid):
        """Recursive helper that fills `grid` completely with valid digits."""
        target = self._find_empty(grid)
        if target is None:
            return True
        row, col = target
        digits = list(range(1, 10))
        self.rng.shuffle(digits)
        for digit in digits:
            if self.solver._is_safe(grid, row, col, digit):
                grid[row][col] = digit
                if self._fill_grid(grid):
                    return True
                grid[row][col] = 0
        return False
    def _find_empty(self, grid):
        """Return the (row, col) of the first empty cell, or None if full."""
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    return (r, c)
        return None
    def _remove_cells(self, puzzle, target):
        """Remove up to `target` digits while keeping the solution unique."""
        cells = [(r, c) for r in range(9) for c in range(9)]
        self.rng.shuffle(cells)
        removed = 0
        for r, c in cells:
            if removed >= target:
                break
            backup = puzzle[r][c]
            puzzle[r][c] = 0
            if self.solver.count_solutions(puzzle, limit=2) == 1:
                removed += 1
            else:
                puzzle[r][c] = backup