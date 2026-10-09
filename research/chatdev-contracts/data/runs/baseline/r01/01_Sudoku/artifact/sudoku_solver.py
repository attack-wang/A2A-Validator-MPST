'''
sudoku_solver.py
Backtracking solver used to (a) verify that generated puzzles have a
solution and (b) count solutions to guarantee uniqueness.
'''
class SudokuSolver:
    """Classic backtracking Sudoku solver with solution counting."""
    SIZE = 9
    BOX_SIZE = 3
    def __init__(self, board):
        # Accept either a SudokuBoard instance or a plain 9x9 nested list.
        if hasattr(board, "grid"):
            self.grid = [list(row) for row in board.grid]
        else:
            self.grid = [list(row) for row in board]
    def solve(self):
        """Solve the board in place. Returns True if a solution was found."""
        return self._backtrack(count_only=False)
    def count_solutions(self, limit=2):
        """
        Count solutions, stopping as soon as `limit` solutions are found.
        Used to verify a generated puzzle has exactly one solution.
        """
        return self._backtrack(count_only=True, limit=limit)
    def get_grid(self):
        return [row[:] for row in self.grid]
    def _backtrack(self, count_only=False, limit=2):
        cell = self._find_empty()
        if cell is None:
            if count_only:
                self._found += 1
                return self._found >= limit
            return True
        row, col = cell
        for value in range(1, self.SIZE + 1):
            if self._is_safe(row, col, value):
                self.grid[row][col] = value
                if self._backtrack(count_only, limit):
                    if not count_only:
                        return True
                    # In count mode keep exploring until the limit is hit;
                    # _backtrack returns True only when the limit is reached.
                    return True
                self.grid[row][col] = 0
        return False
    def _find_empty(self):
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.grid[r][c] == 0:
                    return (r, c)
        return None
    def _is_safe(self, row, col, value):
        for i in range(self.SIZE):
            if self.grid[row][i] == value or self.grid[i][col] == value:
                return False
        br = (row // self.BOX_SIZE) * self.BOX_SIZE
        bc = (col // self.BOX_SIZE) * self.BOX_SIZE
        for r in range(br, br + self.BOX_SIZE):
            for c in range(bc, bc + self.BOX_SIZE):
                if self.grid[r][c] == value:
                    return False
        return True