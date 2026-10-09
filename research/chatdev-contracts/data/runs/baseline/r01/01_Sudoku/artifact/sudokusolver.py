'''
sudoku_solver.py
Backtracking solver used to (a) verify that generated puzzles have a
solution and (b) count solutions to guarantee uniqueness.
'''
class SudokuSolver:
    SIZE = 9
    BOX_SIZE = 3
    def __init__(self, grid):
        self.grid = [list(row) for row in grid]
    def solve(self):
        return self._search(count_mode=False)
    def count_solutions(self, limit=2):
        self._found = 0
        self._limit = limit
        self._search(count_mode=True)
        return self._found
    def get_grid(self):
        return [row[:] for row in self.grid]
    def _search(self, count_mode):
        cell = self._find_empty()
        if cell is None:
            if count_mode:
                self._found += 1
                return self._found >= self._limit
            return True
        row, col = cell
        for value in range(1, self.SIZE + 1):
            if self._is_safe(row, col, value):
                self.grid[row][col] = value
                if self._search(count_mode):
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