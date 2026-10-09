'''
board.py
This module defines the Board class, which models the standard 3x3
tic-tac-toe grid. It is responsible for storing the state of every cell,
validating and applying moves, and detecting winning lines or a full
(draw) board. The Board class contains no user-interface code so that it
can be reused by both the graphical and the console front-ends.
'''
class Board:
    """Models a 3x3 tic-tac-toe board and its rules about placement."""
    SIZE = 3
    EMPTY = " "
    # All index triples that form a winning line (rows, columns, diagonals).
    WINNING_LINES = [
        # Rows
        ((0, 0), (0, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),
        # Columns
        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2)),
        # Diagonals
        ((0, 0), (1, 1), (2, 2)),
        ((0, 2), (1, 1), (2, 0)),
    ]
    def __init__(self):
        """Create an empty 3x3 board."""
        self.reset()
    def reset(self):
        """Clear the board so a fresh round can start."""
        self._grid = [[self.EMPTY for _ in range(self.SIZE)]
                      for _ in range(self.SIZE)]
    def is_valid_position(self, row, col):
        """Return True if (row, col) lies inside the 3x3 grid."""
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE
    def is_cell_empty(self, row, col):
        """Return True if the given cell is inside the grid and empty."""
        if not self.is_valid_position(row, col):
            return False
        return self._grid[row][col] == self.EMPTY
    def place_mark(self, row, col, mark):
        """
        Put `mark` in cell (row, col).
        Returns True when the move was applied, False when the position is
        outside the grid or the cell is already occupied.
        """
        if not self.is_cell_empty(row, col):
            return False
        self._grid[row][col] = mark
        return True
    def get_cell(self, row, col):
        """Return the mark stored in (row, col) or None if out of range."""
        if not self.is_valid_position(row, col):
            return None
        return self._grid[row][col]
    def get_empty_cells(self):
        """Return a list of (row, col) tuples for every empty cell."""
        return [(r, c)
                for r in range(self.SIZE)
                for c in range(self.SIZE)
                if self._grid[r][c] == self.EMPTY]
    def is_full(self):
        """Return True when no empty cells remain (draw condition)."""
        return len(self.get_empty_cells()) == 0
    def get_winning_line(self):
        """
        Return the winning mark and its line (mark, cells) if a player
        has three in a row, otherwise return (None, None).
        """
        for line in self.WINNING_LINES:
            marks = [self._grid[r][c] for (r, c) in line]
            if marks[0] != self.EMPTY and marks[0] == marks[1] == marks[2]:
                return marks[0], line
        return None, None
    def get_winner(self):
        """Return the mark ('X' or 'O') that completed a line, else None."""
        mark, _ = self.get_winning_line()
        return mark
    def as_text(self):
        """Return a plain-text rendering of the board for console play."""
        rows = []
        for r in range(self.SIZE):
            row_cells = [self._grid[r][c] for c in range(self.SIZE)]
            rows.append(" " + " | ".join(row_cells) + " ")
            if r < self.SIZE - 1:
                rows.append("---+---+---")
        return "\n".join(rows)