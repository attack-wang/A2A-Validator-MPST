'''
sudoku_board.py
Defines the SudokuBoard class, the core data model of the game.
It stores the 9x9 grid, tracks which cells are fixed clues, and
provides validation helpers used for mistake checking and
completion detection.
'''
class SudokuBoard:
    """Represents a 9x9 Sudoku board with validation helpers."""
    SIZE = 9
    BOX_SIZE = 3
    EMPTY = 0
    def __init__(self):
        self.grid = [[self.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.fixed = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]
    def reset(self, puzzle):
        """Load a puzzle (9x9 list of lists, 0 = empty) and mark fixed cells."""
        self.grid = [row[:] for row in puzzle]
        self.fixed = [[puzzle[r][c] != self.EMPTY for c in range(self.SIZE)] for r in range(self.SIZE)]
    def in_bounds(self, row, col):
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE
    def get_value(self, row, col):
        if not self.in_bounds(row, col):
            return self.EMPTY
        return self.grid[row][col]
    def is_fixed(self, row, col):
        if not self.in_bounds(row, col):
            return False
        return self.fixed[row][col]
    def is_empty(self, row, col):
        return self.get_value(row, col) == self.EMPTY
    def set_value(self, row, col, value):
        if not self.in_bounds(row, col) or self.is_fixed(row, col):
            return False
        if not isinstance(value, int) or not (1 <= value <= 9):
            return False
        self.grid[row][col] = value
        return True
    def clear_value(self, row, col):
        if not self.in_bounds(row, col) or self.is_fixed(row, col):
            return False
        self.grid[row][col] = self.EMPTY
        return True
    def is_valid_placement(self, row, col, value):
        # ... same as before
    def find_conflicts(self):
        # ... same
    def is_complete(self):
        # ... same
    def is_full(self):
        # ... same
    def find_empty(self):
        """Return (row, col) of the first empty cell, or None if the board is full."""
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.grid[r][c] == self.EMPTY:
                    return (r, c)
        return None
    def get_row(self, row):
        return list(self.grid[row])
    def get_column(self, col):
        return [self.grid[r][col] for r in range(self.SIZE)]
    def get_box(self, row, col):
        box_row, box_col = (row // self.BOX_SIZE) * self.BOX_SIZE, (col // self.BOX_SIZE) * self.BOX_SIZE
        return [self.grid[r][c] for r in range(box_row, box_row + self.BOX_SIZE) for c in range(box_col, box_col + self.BOX_SIZE)]