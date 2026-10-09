'''
sudokusolver.py
Backtracking solver used both to build puzzles and to verify uniqueness.
'''
import random
class SudokuSolver:
    """Backtracking solver used both to build puzzles and to verify them."""
    @staticmethod
    def find_empty(grid):
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    return r, c
        return None
    @staticmethod
    def _is_safe(grid, row, col, value):
        """True if `value` does not clash in grid[row][col]'s row,
        column or 3x3 box. The target cell is assumed to be empty."""
        for i in range(9):
            if grid[row][i] == value or grid[i][col] == value:
                return False
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if grid[r][c] == value:
                    return False
        return True
    @classmethod
    def solve(cls, grid, randomize=False):
        """Solve in place; return True if a solution was found."""
        empty = cls.find_empty(grid)
        if empty is None:
            return True
        row, col = empty
        digits = list(range(1, 10))
        if randomize:
            random.shuffle(digits)
        for value in digits:
            if cls._is_safe(grid, row, col, value):
                grid[row][col] = value
                if cls.solve(grid, randomize):
                    return True
                grid[row][col] = 0
        return False
    @classmethod
    def count_solutions(cls, grid, limit=2):
        """Count solutions up to `limit`; used to guarantee uniqueness."""
        empty = cls.find_empty(grid)
        if empty is None:
            return 1
        row, col = empty
        total = 0
        for value in range(1, 10):
            if cls._is_safe(grid, row, col, value):
                grid[row][col] = value
                total += cls.count_solutions(grid, limit)
                grid[row][col] = 0
                if total >= limit:
                    break
        return total