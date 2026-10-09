'''
puzzle_generator.py
Generates Sudoku puzzles with unique solutions at several difficulty
levels by filling a complete board randomly and then removing clues
while the puzzle still admits exactly one solution.
'''
import random
from sudoku_solver import SudokuSolver
class PuzzleGenerator:
    DIFFICULTY_LEVELS = {
        "easy": 38,
        "medium": 32,
        "hard": 28,
    }
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    def generate(self, difficulty="medium"):
        """Return (board, solution) for a new puzzle with a unique solution."""
        target_clues = self.DIFFICULTY_LEVELS.get(
            difficulty, self.DIFFICULTY_LEVELS["medium"])
        solution = self._generate_full_board()
        puzzle = [row[:] for row in solution]
        cells = [(r, c) for r in range(9) for c in range(9)]
        self.rng.shuffle(cells)
        removed = 0
        max_removals = 81 - target_clues
        for row, col in cells:
            if removed >= max_removals:
                break
            backup = puzzle[row][col]
            puzzle[row][col] = 0
            solver = SudokuSolver(puzzle)
            if solver.count_solutions(limit=2) != 1:
                puzzle[row][col] = backup  # keep uniqueness
            else:
                removed += 1
        return puzzle, solution
    def _generate_full_board(self):
        """Create a complete, valid 9x9 Sudoku grid via randomized backtracking."""
        grid = [[0] * 9 for _ in range(9)]
        self._fill_grid(grid)
        return grid
    def _fill_grid(self, grid):
        numbers = list(range(1, 10))
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    self.rng.shuffle(numbers)
                    for value in numbers:
                        if self._is_safe(grid, r, c, value):
                            grid[r][c] = value
                            if self._fill_grid(grid):
                                return True
                            grid[r][c] = 0
                    return False
        return True
    @staticmethod
    def _is_safe(grid, row, col, value):
        for i in range(9):
            if grid[row][i] == value or grid[i][col] == value:
                return False
        br = (row // 3) * 3
        bc = (col // 3) * 3
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if grid[r][c] == value:
                    return False
        return True