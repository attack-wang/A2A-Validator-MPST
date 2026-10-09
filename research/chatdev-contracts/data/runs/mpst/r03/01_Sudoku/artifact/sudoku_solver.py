'''
SudokuSolver: backtracking solver with an MRV (minimum remaining values)
heuristic. Provides grid solving, solution counting (for uniqueness
checks during puzzle generation) and placement validation helpers.
'''
class SudokuSolver:
    EMPTY = 0
    @staticmethod
    def is_valid_placement(grid, row, col, value):
        """Return True if placing `value` at (row, col) violates no row/column/box rule."""
        if value == SudokuSolver.EMPTY:
            return False
        if any(grid[row][c] == value for c in range(9) if c != col):
            return False
        if any(grid[r][col] == value for r in range(9) if r != row):
            return False
        br, bc = (row // 3) * 3, (col // 3) * 3
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if (r, c) != (row, col) and grid[r][c] == value:
                    return False
        return True
    @staticmethod
    def find_empty(grid):
        """Return (row, col) of the first empty cell, or None if grid is full."""
        for r in range(9):
            for c in range(9):
                if grid[r][c] == SudokuSolver.EMPTY:
                    return (r, c)
        return None
    @staticmethod
    def find_empty_with_mrv(grid):
        """Return (row, col, candidates) for the empty cell with fewest candidates, or None."""
        best = None
        for r in range(9):
            for c in range(9):
                if grid[r][c] == SudokuSolver.EMPTY:
                    candidates = [v for v in range(1, 10)
                                  if SudokuSolver.is_valid_placement(grid, r, c, v)]
                    if best is None or len(candidates) < len(best[2]):
                        best = (r, c, candidates)
                        if len(candidates) <= 1:
                            return best
        return best
    @staticmethod
    def count_solutions(grid, limit=2):
        """Count solutions up to `limit`; used by the generator for uniqueness checks."""
        def _solve():
            cell = SudokuSolver.find_empty_with_mrv(grid)
            if cell is None:
                return 1
            r, c, candidates = cell
            if not candidates:
                return 0
            count = 0
            for v in candidates:
                grid[r][c] = v
                count += _solve()
                grid[r][c] = SudokuSolver.EMPTY
                if count >= limit:
                    break
            return count
        return _solve()