'''
sudoku_solver.py
Backtracking solver used by the generator to verify that generated
puzzles have exactly one solution, and to compute solutions quickly.
'''
class SudokuSolver:
    """Backtracking solver for 9x9 Sudoku boards."""
    SIZE = 9
    BOX_SIZE = 3
    @staticmethod
    def find_empty(grid):
        """Return (row, col) of the first empty cell, or None if the grid is full."""
        for r in range(SudokuSolver.SIZE):
            for c in range(SudokuSolver.SIZE):
                if grid[r][c] == 0:
                    return (r, c)
        return None
    @staticmethod
    def is_safe(grid, row, col, value):
        """Check that `value` can be placed at (row, col) without conflicts."""
        # Row and column
        for i in range(SudokuSolver.SIZE):
            if grid[row][i] == value or grid[i][col] == value:
                return False
        # 3x3 subgrid
        box_row, box_col = (row // SudokuSolver.BOX_SIZE) * SudokuSolver.BOX_SIZE, (col // SudokuSolver.BOX_SIZE) * SudokuSolver.BOX_SIZE
        for r in range(box_row, box_row + SudokuSolver.BOX_SIZE):
            for c in range(box_col, box_col + SudokuSolver.BOX_SIZE):
                if grid[r][c] == value:
                    return False
        return True
    @classmethod
    def count_solutions(cls, grid, limit=2):
        """
        Count solutions of `grid` up to `limit` (default 2) using backtracking.
        Returns the number of solutions found (capped at `limit`).
        """
        grid_copy = [row[:] for row in grid]
        count = [0]
        def backtrack():
            empty = cls.find_empty(grid_copy)
            if empty is None:
                count[0] += 1
                return count[0] >= limit
            row, col = empty
            for value in range(1, 10):
                if cls.is_safe(grid_copy, row, col, value):
                    grid_copy[row][col] = value
                    if backtrack():
                        grid_copy[row][col] = 0
                        return True
                    grid_copy[row][col] = 0
            return False
        backtrack()
        return count[0]
    @classmethod
    def solve(cls, grid):
        """
        Solve the puzzle in-place if possible.
        Returns True and fills `grid` with the solution, or False if unsolvable.
        """
        empty = cls.find_empty(grid)
        if empty is None:
            return True
        row, col = empty
        for value in range(1, 10):
            if cls.is_safe(grid, row, col, value):
                grid[row][col] = value
                if cls.solve(grid):
                    return True
                grid[row][col] = 0
        return False