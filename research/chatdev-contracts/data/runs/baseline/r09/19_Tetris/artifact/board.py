'''
board.py
Defines the Board class: the 10x20 playfield.
Responsibilities:
  * store locked-in cells,
  * validate candidate positions for a falling tetromino,
  * lock pieces into the grid,
  * detect and clear completed lines,
  * decide whether the game is over.
'''
from settings import COLS, ROWS
class Board:
    """The Tetris playfield grid."""
    def __init__(self):
        self.reset()
    def reset(self):
        """Empty the grid; each cell holds a color tuple or None."""
        self.grid = [[None] * COLS for _ in range(ROWS)]
    def is_inside(self, col, row):
        """True if (col, row) lies within the board boundaries."""
        return 0 <= col < COLS and 0 <= row < ROWS
    def cell_free(self, col, row):
        """True if the cell is inside the board and not occupied."""
        return self.is_inside(col, row) and self.grid[row][col] is None
    def is_valid_position(self, tetromino, dx=0, dy=0, matrix=None):
        """
        True if the tetromino, moved by (dx, dy) and optionally using
        `matrix` as its shape, fits entirely in free space on the board.
        """
        for col, row in tetromino.cells(dx, dy, matrix):
            if not self.cell_free(col, row):
                return False
        return True
    def lock_piece(self, tetromino):
        """Write the tetromino's cells into the grid using its color."""
        for col, row in tetromino.cells():
            self.grid[row][col] = tetromino.color
    def clear_lines(self):
        """
        Remove all fully occupied rows.
        Returns the number of rows cleared.
        """
        remaining = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = ROWS - len(remaining)
        while len(remaining) < ROWS:
            remaining.insert(0, [None] * COLS)
        self.grid = remaining
        return cleared
    def is_game_over(self, tetromino):
        """True if the freshly spawned tetromino overlaps existing blocks."""
        return not self.is_valid_position(tetromino)