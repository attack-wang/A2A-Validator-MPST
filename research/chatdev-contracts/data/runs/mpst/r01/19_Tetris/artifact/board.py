'''
Defines the Board class: the 10x20 playfield grid that stores locked cells,
validates piece positions and clears completed lines.
'''
from constants import BOARD_COLS, BOARD_ROWS
class Board:
    """Playfield grid holding locked cell colors and providing collision/line logic."""
    def __init__(self):
        """Create an empty board (every cell holds None = no locked block)."""
        self.grid = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
    def is_valid_position(self, cells):
        """
        Return True if every (x, y) cell coordinate is a legal position:
        inside the side/bottom walls and not overlapping a locked cell.
        Cells above the top edge (y < 0) are tolerated for rotation kicks.
        """
        for x, y in cells:
            if x < 0 or x >= BOARD_COLS:
                return False
            if y >= BOARD_ROWS:
                return False
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True
    def lock_piece(self, tetromino):
        """
        Write the tetromino's cells into the grid as locked cells (colored).
        Returns True if any part of the piece locked above the top row,
        which signals a lock-out game over.
        """
        locked_out = False
        for x, y in tetromino.get_cells():
            if y < 0:
                locked_out = True
            elif 0 <= x < BOARD_COLS:
                self.grid[y][x] = tetromino.color
        return locked_out
    def clear_lines(self):
        """
        Remove every fully occupied row, shifting the rows above down.
        Returns the number of cleared lines (0-4).
        """
        remaining = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = BOARD_ROWS - len(remaining)
        while len(remaining) < BOARD_ROWS:
            remaining.insert(0, [None] * BOARD_COLS)
        self.grid = remaining
        return cleared
    def is_empty(self):
        """Return True when no blocks are locked on the board."""
        return all(cell is None for row in self.grid for cell in row)