'''
puzzle_generator.py
Generates random, uniquely solvable Sudoku puzzles at several difficulty
levels. A complete solution is produced with a randomized backtracking
search, then clues are removed one by one while a solution counter keeps
the puzzle guaranteed to have exactly one solution.
'''
import random
from sudoku_board import SudokuBoard
class PuzzleGenerator:
    """Creates full Sudoku solutions and carves puzzles out of them."""
    DIFFICULTY_LEVELS = {
        "easy": 38,      # number of clues to keep (approx.)
        "medium": 32,
        "hard": 27,
    }
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    # ------------------------------------------------------------------ #
    # Solution generation
    # ------------------------------------------------------------------ #
    def generate_full_solution(self):
        """Produce a complete, valid 9x9 Sudoku grid via randomized backtracking."""
        grid = [[SudokuBoard.EMPTY for _ in range(SudokuBoard.SIZE)]
                for _ in range(SudokuBoard.SIZE)]
        self._fill_grid(grid)
        return grid
    def _fill_grid(self, grid):
        """Recursive backtracking filler; returns True when grid is complete."""
        target = self._find_empty(grid)
        if target is None:
            return True
        row, col = target
        digits = list(range(1, 10))
        self.rng.shuffle(digits)
        for digit in digits:
            if self._is_safe(grid, row, col, digit):
                grid[row][col] = digit
                if self._fill_grid(grid):
                    return True
                grid[row][col] = SudokuBoard.EMPTY
        return False
    @staticmethod
    def _find_empty(grid):
        """Return coordinates of the first empty cell, or None."""
        for r in range(SudokuBoard.SIZE):
            for c in range(SudokuBoard.SIZE):
                if grid[r][c] == SudokuBoard.EMPTY:
                    return r, c
        return None
    @staticmethod
    def _is_safe(grid, row, col, value):
        """Check row/column/box constraints for a candidate value."""
        for c in range(SudokuBoard.SIZE):
            if grid[row][c] == value:
                return False
        for r in range(SudokuBoard.SIZE):
            if grid[r][col] == value:
                return False
        box_row = (row // SudokuBoard.BOX_SIZE) * SudokuBoard.BOX_SIZE
        box_col = (col // SudokuBoard.BOX_SIZE) * SudokuBoard.BOX_SIZE
        for r in range(box_row, box_row + SudokuBoard.BOX_SIZE):
            for c in range(box_col, box_col + SudokuBoard.BOX_SIZE):
                if grid[r][c] == value:
                    return False
        return True
    # ------------------------------------------------------------------ #
    # Puzzle carving
    # ------------------------------------------------------------------ #
    def generate_puzzle(self, difficulty="medium"):
        """
        Create a puzzle with a unique solution.
        Returns (puzzle_grid, solution_grid).
        """
        if difficulty not in self.DIFFICULTY_LEVELS:
            raise ValueError(f"Unknown difficulty: {difficulty}")
        solution = self.generate_full_solution()
        puzzle = [row[:] for row in solution]
        target_clues = self.DIFFICULTY_LEVELS[difficulty]
        cells = [(r, c) for r in range(SudokuBoard.SIZE) for c in range(SudokuBoard.SIZE)]
        self.rng.shuffle(cells)
        clues = SudokuBoard.SIZE * SudokuBoard.SIZE
        for r, c in cells:
            if clues <= target_clues:
                break
            removed = puzzle[r][c]
            puzzle[r][c] = SudokuBoard.EMPTY
            if self._count_solutions(puzzle, limit=2) != 1:
                puzzle[r][c] = removed  # restore to keep uniqueness
            else:
                clues -= 1
        return puzzle, solution
    def _count_solutions(self, grid, limit=2):
        """Count solutions up to `limit` using backtracking."""
        target = self._find_empty(grid)
        if target is None:
            return 1
        row, col = target
        count = 0
        for digit in range(1, 10):
            if self._is_safe(grid, row, col, digit):
                grid[row][col] = digit
                count += self._count_solutions(grid, limit)
                grid[row][col] = SudokuBoard.EMPTY
                if count >= limit:
                    break
        return count