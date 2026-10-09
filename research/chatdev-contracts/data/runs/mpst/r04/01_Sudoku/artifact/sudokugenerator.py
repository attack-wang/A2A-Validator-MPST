'''
sudokugenerator.py
Generates random Sudoku puzzles with a unique solution at three
difficulty levels (Easy / Medium / Hard).
'''
import random
from sudokusolver import SudokuSolver
class SudokuGenerator:
    """Generates random Sudoku puzzles with a unique solution."""
    DIFFICULTY_LEVELS = {
        "Easy": 38,      # givens remaining
        "Medium": 32,
        "Hard": 27,
    }
    def generate(self, difficulty="Medium"):
        """Return (puzzle, solution) as 9x9 lists; 0 marks an empty cell."""
        target_givens = self.DIFFICULTY_LEVELS.get(difficulty, 32)
        solution = self._generate_full_grid()
        puzzle = [row[:] for row in solution]
        self._remove_cells(puzzle, target_givens)
        return puzzle, solution
    def _generate_full_grid(self):
        grid = [[0] * 9 for _ in range(9)]
        # Fill the three diagonal boxes with random permutations, then solve.
        for box in range(3):
            digits = list(range(1, 10))
            random.shuffle(digits)
            idx = 0
            for r in range(box * 3, box * 3 + 3):
                for c in range(box * 3, box * 3 + 3):
                    grid[r][c] = digits[idx]
                    idx += 1
        SudokuSolver.solve(grid, randomize=True)
        return grid
    def _remove_cells(self, puzzle, target_givens):
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        givens = 81
        for r, c in cells:
            if givens <= target_givens:
                break
            backup = puzzle[r][c]
            puzzle[r][c] = 0
            if SudokuSolver.count_solutions([row[:] for row in puzzle], limit=2) != 1:
                puzzle[r][c] = backup  # restore: removal breaks uniqueness
            else:
                givens -= 1