'''
sudoku_board.py
9x9 Sudoku board: stores the grid and fixed clues, provides
validation helpers used by the GUI.
'''
class SudokuBoard:
    SIZE = 9
    BOX_SIZE = 3
    def __init__(self, grid=None, fixed=None):
        if grid is None:
            self.grid = [[0] * self.SIZE for _ in range(self.SIZE)]
            self.fixed = [[False] * self.SIZE for _ in range(self.SIZE)]
        else:
            self.grid = [list(row) for row in grid]
            self.fixed = ([list(row) for row in fixed]
                          if fixed is not None
                          else [[cell != 0 for cell in row] for row in self.grid])
    def get_cell(self, row, col):
        return self.grid[row][col]
    def set_cell(self, row, col, value):
        if self.fixed[row][col]:
            raise ValueError("Cannot modify a fixed clue cell.")
        self.grid[row][col] = value
    def is_fixed(self, row, col):
        return self.fixed[row][col]
    def is_empty(self, row, col):
        return self.grid[row][col] == 0
    def is_complete(self):
        filled = all(cell != 0 for row in self.grid for cell in row)
        return filled and not self.find_conflicts()
    def find_conflicts(self):
        """Return a set of (row, col) cells violating row/column/box rules."""
        conflicts = set()
        for i in range(self.SIZE):
            row_seen, col_seen = {}, {}
            for j in range(self.SIZE):
                rv = self.grid[i][j]
                if rv:
                    if rv in row_seen:
                        conflicts.update({(i, j), (i, row_seen[rv])})
                    else:
                        row_seen[rv] = j
                cv = self.grid[j][i]
                if cv:
                    if cv in col_seen:
                        conflicts.update({(j, i), (col_seen[cv], i)})
                    else:
                        col_seen[cv] = j
        for br in range(0, self.SIZE, self.BOX_SIZE):
            for bc in range(0, self.SIZE, self.BOX_SIZE):
                box_seen = {}
                for r in range(br, br + self.BOX_SIZE):
                    for c in range(bc, bc + self.BOX_SIZE):
                        v = self.grid[r][c]
                        if v:
                            if v in box_seen:
                                conflicts.update({(r, c), box_seen[v]})
                            else:
                                box_seen[v] = (r, c)
        return conflicts
    def copy(self):
        clone = SudokuBoard.__new__(SudokuBoard)
        clone.grid = [row[:] for row in self.grid]
        clone.fixed = [row[:] for row in self.fixed]
        return clone