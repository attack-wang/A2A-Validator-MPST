'''
sudoku_board.py
Core game logic for the Sudoku board: stores the puzzle state, tracks
which cells are editable, validates entries against Sudoku rules
(rows, columns, 3x3 subgrids), detects conflicts, and determines when
the puzzle has been completed correctly.
'''
class SudokuBoard:
    """Holds puzzle state and implements validation / completion logic."""
    SIZE = 9
    BOX = 3
    EMPTY = 0
    def __init__(self, puzzle, solution):
        if not self._valid_shape(puzzle) or not self._valid_shape(solution):
            raise ValueError("Puzzle and solution must be 9x9 grids.")
        self._puzzle = [row[:] for row in puzzle]
        self._solution = [row[:] for row in solution]
        self._values = [row[:] for row in puzzle]
        self._fixed = [[puzzle[r][c] != self.EMPTY for c in range(self.SIZE)]
                       for r in range(self.SIZE)]
    @staticmethod
    def _valid_shape(grid):
        """Return True when grid is a 9x9 list of lists."""
        return (isinstance(grid, list) and len(grid) == SudokuBoard.SIZE and
                all(isinstance(row, list) and len(row) == SudokuBoard.SIZE for row in grid))
    # --- state access -------------------------------------------------
    def get_value(self, row, col):
        """Return the current value (0 for empty) of the given cell."""
        return self._values[row][col]
    def get_board(self):
        """Return a copy of the full current 9x9 grid."""
        return [row[:] for row in self._values]
    def is_fixed(self, row, col):
        """Return True when the cell is a given clue and not editable."""
        return self._fixed[row][col]
    def get_solution_value(self, row, col):
        """Return the correct solution value for the given cell."""
        return self._solution[row][col]
    # --- mutation -----------------------------------------------------
    def set_value(self, row, col, value):
        """Set an editable cell to value; return True on success."""
        if self._fixed[row][col]:
            return False
        if value == self.EMPTY:
            self._values[row][col] = self.EMPTY
            return True
        if not isinstance(value, int) or not 1 <= value <= 9:
            return False
        self._values[row][col] = value
        return True
    def clear_value(self, row, col):
        """Empty an editable cell; fixed clues are left untouched."""
        if not self._fixed[row][col]:
            self._values[row][col] = self.EMPTY
    def reset(self):
        """Restore the board to the original puzzle clues."""
        self._values = [row[:] for row in self._puzzle]
    # --- validation ---------------------------------------------------
    def _same_box(self, r1, c1, r2, c2):
        """Return True when two cells share the same 3x3 subgrid."""
        return (r1 // self.BOX == r2 // self.BOX) and (c1 // self.BOX == c2 // self.BOX)
    def find_conflicts(self):
        """Return set of (row, col) cells that violate row/col/box rules."""
        conflicts = set()
        # rows
        for r in range(self.SIZE):
            seen = {}
            for c in range(self.SIZE):
                v = self._values[r][c]
                if v != self.EMPTY:
                    if v in seen:
                        conflicts.add((r, c))
                        conflicts.add((r, seen[v]))
                    else:
                        seen[v] = c
        # cols
        for c in range(self.SIZE):
            seen = {}
            for r in range(self.SIZE):
                v = self._values[r][c]
                if v != self.EMPTY:
                    if v in seen:
                        conflicts.add((r, c))
                        conflicts.add((seen[v], c))
                    else:
                        seen[v] = r
        # boxes
        for br in range(0, self.SIZE, self.BOX):
            for bc in range(0, self.SIZE, self.BOX):
                seen = {}
                for r in range(br, br + self.BOX):
                    for c in range(bc, bc + self.BOX):
                        v = self._values[r][c]
                        if v != self.EMPTY:
                            if v in seen:
                                conflicts.add((r, c))
                                conflicts.add(seen[v])
                            else:
                                seen[v] = (r, c)
        return conflicts
    def has_conflict(self, row, col):
        """Return True when the given cell currently breaks a Sudoku rule."""
        return (row, col) in self.find_conflicts()
    def is_correct(self, row, col):
        """Return True when the cell's value matches the solution."""
        return self._values[row][col] == self._solution[row][col]
    def find_incorrect_cells(self):
        """Cells filled by the player whose value differs from the solution."""
        return {(r, c) for r in range(self.SIZE) for c in range(self.SIZE)
                if not self._fixed[r][c] and self._values[r][c] != self.EMPTY
                and self._values[r][c] != self._solution[r][c]}
    def is_filled(self):
        """Return True when no cell is empty."""
        return all(self._values[r][c] != self.EMPTY
                   for r in range(self.SIZE) for c in range(self.SIZE))
    def is_complete(self):
        """True when every cell is filled and every row/col/box has 1-9 exactly once."""
        if not self.is_filled():
            return False
        target = set(range(1, 10))
        for r in range(self.SIZE):
            if set(self._values[r]) != target:
                return False
        for c in range(self.SIZE):
            if {self._values[r][c] for r in range(self.SIZE)} != target:
                return False
        for br in range(0, self.SIZE, self.BOX):
            for bc in range(0, self.SIZE, self.BOX):
                box = {self._values[r][c]
                       for r in range(br, br + self.BOX)
                       for c in range(bc, bc + self.BOX)}
                if box != target:
                    return False
        return True