'''
sudoku_logic.py
Core Sudoku board model for the 9x9 puzzle game.
Stores the original puzzle (givens), the unique solution and the
player's current entries, and provides all validation helpers used
by the GUI: rule-based placement checks, real-time conflict
detection, mistake counting and completion confirmation.
'''
class SudokuBoard:
    """9x9 Sudoku board holding puzzle state, solution and validation."""
    SIZE = 9
    def __init__(self):
        self.puzzle = [[0] * self.SIZE for _ in range(self.SIZE)]    # givens + user entries
        self.solution = [[0] * self.SIZE for _ in range(self.SIZE)]  # full solution
        self.given = [[False] * self.SIZE for _ in range(self.SIZE)] # True for fixed cells
    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def load_puzzle(self, puzzle, solution):
        """Load a new puzzle (0 = empty cell) and its unique solution."""
        self.puzzle = [row[:] for row in puzzle]
        self.solution = [row[:] for row in solution]
        self.given = [[self.puzzle[r][c] != 0 for c in range(self.SIZE)]
                      for r in range(self.SIZE)]
    # ------------------------------------------------------------------
    # Basic queries
    # ------------------------------------------------------------------
    @staticmethod
    def in_bounds(row, col):
        """True if (row, col) lies inside the 9x9 grid."""
        return 0 <= row < 9 and 0 <= col < 9
    def is_given(self, row, col):
        """True if the cell is one of the original puzzle clues."""
        return self.given[row][col]
    def get_value(self, row, col):
        """Current digit in the cell (0 = empty)."""
        return self.puzzle[row][col]
    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------
    def set_value(self, row, col, value):
        """Place a digit in a non-given cell; givens are protected."""
        if self.in_bounds(row, col) and not self.given[row][col]:
            self.puzzle[row][col] = value
    def clear_value(self, row, col):
        """Empty a non-given cell; givens are protected."""
        if self.in_bounds(row, col) and not self.given[row][col]:
            self.puzzle[row][col] = 0
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def is_valid_placement(self, row, col, value):
        """True if `value` at (row, col) breaks no row/column/box rule,
        ignoring the cell's own current content."""
        for i in range(9):
            if i != col and self.puzzle[row][i] == value:
                return False
            if i != row and self.puzzle[i][col] == value:
                return False
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) != (row, col) and self.puzzle[r][c] == value:
                    return False
        return True
    def find_conflicts(self):
        """Return a set of (row, col) cells that duplicate a digit within
        their row, column or 3x3 box."""
        conflicts = set()
        units = []
        for i in range(9):
            units.append([(i, c) for c in range(9)])                  # row i
            units.append([(r, i) for r in range(9)])                  # column i
            br, bc = (i // 3) * 3, (i % 3) * 3
            units.append([(br + r, bc + c) for r in range(3) for c in range(3)])
        for unit in units:
            seen = {}
            for r, c in unit:
                v = self.puzzle[r][c]
                if v != 0:
                    if v in seen:
                        conflicts.add((r, c))
                        conflicts.add(seen[v])
                    else:
                        seen[v] = (r, c)
        return conflicts
    def count_filled(self):
        """Number of cells currently holding a digit."""
        return sum(1 for r in range(9) for c in range(9) if self.puzzle[r][c] != 0)
    def count_mistakes(self):
        """Number of user entries that differ from the stored solution."""
        return sum(
            1 for r in range(9) for c in range(9)
            if not self.given[r][c]
            and self.puzzle[r][c] != 0
            and self.puzzle[r][c] != self.solution[r][c]
        )
    def is_complete(self):
        """True when every cell is filled and every row, column and 3x3
        box contains the digits 1-9 exactly once."""
        if any(self.puzzle[r][c] == 0 for r in range(9) for c in range(9)):
            return False
        target = set(range(1, 10))
        for i in range(9):
            if set(self.puzzle[i]) != target:
                return False
            if {self.puzzle[r][i] for r in range(9)} != target:
                return False
            br, bc = (i // 3) * 3, (i % 3) * 3
            if {self.puzzle[br + r][bc + c] for r in range(3) for c in range(3)} != target:
                return False
        return True