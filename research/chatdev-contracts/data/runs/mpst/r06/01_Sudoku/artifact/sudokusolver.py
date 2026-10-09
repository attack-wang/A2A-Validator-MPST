'''
sudokusolver.py
Backtracking solver for 9x9 Sudoku grids.
SudokuSolver can complete a partially filled grid, and can count the
number of distinct solutions (up to a limit) which the puzzle generator
uses to guarantee every generated puzzle has a unique solution.
'''
class SudokuSolver:
    """Backtracking solver and solution counter for 9x9 Sudoku grids."""
    GRID_SIZE = 9
    SUBGRID_SIZE = 3
    def solve(self, grid):
        """Solve `grid` in place using backtracking. Return True if solved."""
        empty = self._find_empty(grid)
        if empty is None:
            return True
        row, col = empty
        for value in range(1, 10):
            if self._is_safe(grid, row, col, value):
                grid[row][col] = value
                if self.solve(grid):
                    return True
                grid[row][col] = 0
        return False
    def count_solutions(self, grid, limit=2):
        """Count solutions (up to limit) without modifying the input."""
        work = [row[:] for row in grid]
        return self._count(work, limit)
    def _count(self, grid, limit):
        """Recursive helper that counts solutions of `grid` up to `limit`."""
        empty = self._find_empty(grid)
        if empty is None:
            return 1
        row, col = empty
        total = 0
        for value in range(1, 10):
            if self._is_safe(grid, row, col, value):
                grid[row][col] = value
                total += self._count(grid, limit)
                grid[row][col] = 0
                if total >= limit:
                    break
        return total
    def _find_empty(self, grid):
        """Return the (row, col) of the first empty cell, or None if full."""
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                if grid[r][c] == 0:
                    return (r, c)
        return None
    def _is_safe(self, grid, row, col, value):
        """Return True if `value` can be placed at (row, col) without conflict."""
        # Row check
        if any(grid[row][c] == value for c in range(self.GRID_SIZE)):
            return False
        # Column check
        if any(grid[r][col] == value for r in range(self.GRID_SIZE)):
            return False
        # 3x3 subgrid check
        box_row = (row // self.SUBGRID_SIZE) * self.SUBGRID_SIZE
        box_col = (col // self.SUBGRID_SIZE) * self.SUBGRID_SIZE
        for r in range(box_row, box_row + self.SUBGRID_SIZE):
            for c in range(box_col, box_col + self.SUBGRID_SIZE):
                if grid[r][c] == value:
                    return False
        return True