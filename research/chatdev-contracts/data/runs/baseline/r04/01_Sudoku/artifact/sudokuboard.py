class SudokuBoard:
    """Mutable state of a Sudoku game: the 9x9 grid, which cells are
    fixed clues, rule validation, conflict detection and completion tests."""
    SIZE = 9
    def __init__(self, puzzle=None, solution=None):
        """Create a board from an optional 9x9 `puzzle` (0 = empty cell)
        and an optional known `solution`."""
        if puzzle is None:
            puzzle = [[0] * self.SIZE for _ in range(self.SIZE)]
        self.grid = [list(row) for row in puzzle]
        self.solution = [list(row) for row in solution] if solution else None
        self.fixed = [[self.grid[r][c] != 0 for c in range(self.SIZE)]
                      for r in range(self.SIZE)]
    def in_bounds(self, row, col):
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE
    def get_cell(self, row, col):
        return self.grid[row][col]
    def is_fixed(self, row, col):
        return self.fixed[row][col]
    def set_cell(self, row, col, value):
        """Place `value` (1-9) in an editable cell; 0 clears it.
        Returns True if the board was modified."""
        if self.fixed[row][col]:
            return False
        if value not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
            return False
        self.grid[row][col] = value
        return True
    def clear_cell(self, row, col):
        return self.set_cell(row, col, 0)
    def clear_user_entries(self):
        """Reset every editable cell to empty (fixed clues are kept)."""
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if not self.fixed[r][c]:
                    self.grid[r][c] = 0
    def is_valid_placement(self, row, col, value):
        """True if `value` may be placed at (row, col) without breaking
        the row/column/subgrid rules (the cell's own current value is
        ignored during the check)."""
        if value == 0:
            return True
        for c in range(self.SIZE):
            if c != col and self.grid[row][c] == value:
                return False
        for r in range(self.SIZE):
            if r != row and self.grid[r][col] == value:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r != row or c != col) and self.grid[r][c] == value:
                    return False
        return True
    def find_conflicts(self):
        """Return a set of (row, col) tuples for every cell that shares
        a duplicate value within its row, column or 3x3 subgrid."""
        conflicts = set()
        units = self._all_units()
        for unit in units:
            positions = {}
            for (r, c) in unit:
                value = self.grid[r][c]
                if value != 0:
                    positions.setdefault(value, []).append((r, c))
            for cells in positions.values():
                if len(cells) > 1:
                    conflicts.update(cells)
        return conflicts
    def _all_units(self):
        units = []
        for r in range(self.SIZE):  # rows
            units.append([(r, c) for c in range(self.SIZE)])
        for c in range(self.SIZE):  # columns
            units.append([(r, c) for r in range(self.SIZE)])
        for br in range(0, self.SIZE, 3):  # 3x3 subgrids
            for bc in range(0, self.SIZE, 3):
                units.append([(br + i, bc + j) for i in range(3) for j in range(3)])
        return units
    def is_complete(self):
        """True when every cell contains a digit from 1 to 9."""
        return all(self.grid[r][c] != 0
                   for r in range(self.SIZE) for c in range(self.SIZE))
    def is_solved(self):
        """True when the board is completely filled and contains no
        rule violations (i.e. it is a valid solution)."""
        return self.is_complete() and not self.find_conflicts()
    def count_filled(self):
        return sum(1 for r in range(self.SIZE) for c in range(self.SIZE)
                   if self.grid[r][c] != 0)
    def count_empty(self):
        return self.SIZE * self.SIZE - self.count_filled()