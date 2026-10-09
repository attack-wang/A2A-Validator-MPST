'''
sudoku_board.py
Defines the SudokuBoard class, which represents the 9x9 Sudoku grid.
It stores the current values, tracks which cells are pre-filled "givens",
validates placements against Sudoku rules, detects conflicts (mistakes),
and determines whether the puzzle has been completed correctly.
'''
class SudokuBoard:
    """Represents a 9x9 Sudoku board with validation and completion logic."""
    SIZE = 9
    BOX_SIZE = 3
    EMPTY = 0
    def __init__(self):
        """Initialize an empty board with no pre-filled (given) cells."""
        self.grid = [[self.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.given = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]
    def reset(self):
        """Clear the entire board and all given-cell flags."""
        self.grid = [[self.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.given = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]
    def in_bounds(self, row, col):
        """Return True if (row, col) lies within the 9x9 grid."""
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE
    def get_value(self, row, col):
        """Return the value stored at (row, col); 0 means empty."""
        if self.in_bounds(row, col):
            return self.grid[row][col]
        return self.EMPTY
    def is_given(self, row, col):
        """Return True if the cell at (row, col) is a pre-filled given."""
        if self.in_bounds(row, col):
            return self.given[row][col]
        return False
    def set_given(self, row, col, value):
        """Place a value and mark it as a pre-filled given cell."""
        if self.in_bounds(row, col) and self._is_valid_digit(value):
            self.grid[row][col] = value
            self.given[row][col] = True
    def set_value(self, row, col, value):
        """Set a player-entered value at (row, col)."""
        if not self.in_bounds(row, col):
            return False
        if self.given[row][col]:
            return False
        if value == self.EMPTY:
            self.grid[row][col] = self.EMPTY
            return True
        if not self._is_valid_digit(value):
            return False
        self.grid[row][col] = value
        return True
    def clear_cell(self, row, col):
        """Clear a cell if it is not a given. Returns True if cleared."""
        if self.in_bounds(row, col) and not self.given[row][col]:
            self.grid[row][col] = self.EMPTY
            return True
        return False
    def _is_valid_digit(self, value):
        """Return True if value is an integer between 1 and 9."""
        return isinstance(value, int) and 1 <= value <= 9
    def find_conflicts(self):
        """Find all cells that participate in a rule violation."""
        conflicts = set()
        # rows
        for row in range(self.SIZE):
            seen = {}
            for col in range(self.SIZE):
                value = self.grid[row][col]
                if value == self.EMPTY:
                    continue
                if value in seen:
                    conflicts.add((row, col))
                    conflicts.add((row, seen[value]))
                else:
                    seen[value] = col
        # cols
        for col in range(self.SIZE):
            seen = {}
            for row in range(self.SIZE):
                value = self.grid[row][col]
                if value == self.EMPTY:
                    continue
                if value in seen:
                    conflicts.add((row, col))
                    conflicts.add((seen[value], col))
                else:
                    seen[value] = row
        # boxes
        for box_row in range(0, self.SIZE, self.BOX_SIZE):
            for box_col in range(0, self.SIZE, self.BOX_SIZE):
                seen = {}
                for r in range(box_row, box_row + self.BOX_SIZE):
                    for c in range(box_col, box_col + self.BOX_SIZE):
                        value = self.grid[r][c]
                        if value == self.EMPTY:
                            continue
                        if value in seen:
                            conflicts.add((r, c))
                            conflicts.add(seen[value])
                        else:
                            seen[value] = (r, c)
        return conflicts
    def count_empty(self):
        """Return the number of empty cells on the board."""
        return sum(1 for r in range(self.SIZE) for c in range(self.SIZE) if self.grid[r][c] == self.EMPTY)
    def is_full(self):
        """Return True if every cell contains a non-zero value."""
        return all(self.grid[r][c] != self.EMPTY for r in range(self.SIZE) for c in range(self.SIZE))
    def is_solved(self):
        """Return True if the board is full and free of conflicts."""
        return self.is_full() and not self.find_conflicts()