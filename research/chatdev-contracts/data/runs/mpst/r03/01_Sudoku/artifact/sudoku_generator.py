'''
SudokuGenerator: generates full valid grids and carves out puzzles
with unique solutions at various difficulty levels.
'''
import random
from sudoku_solver import SudokuSolver
class SudokuGenerator:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    def generate_full_grid(self):
        grid = [[0] * 9 for _ in range(9)]
        self._fill_grid(grid)
        return grid
    def _fill_grid(self, grid):
        empty = SudokuSolver.find_empty(grid)
        if not empty:
            return True
        row, col = empty
        values = list(range(1, 10))
        self.rng.shuffle(values)
        for value in values:
            if SudokuSolver.is_valid_placement(grid, row, col, value):
                grid[row][col] = value
                if self._fill_grid(grid):
                    return True
                grid[row][col] = 0
        return False
    def generate_puzzle(self, holes=45):
        solution = self.generate_full_grid()
        puzzle = [row[:] for row in solution]
        cells = [(r, c) for r in range(9) for c in range(9)]
        self.rng.shuffle(cells)
        removed = 0
        for r, c in cells:
            if removed >= holes:
                break
            backup = puzzle[r][c]
            puzzle[r][c] = 0
            test = [row[:] for row in puzzle]
            if SudokuSolver.count_solutions(test, limit=2) == 1:
                removed += 1
            else:
                puzzle[r][c] = backup
        return puzzle, solution