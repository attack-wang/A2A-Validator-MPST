"""
board.py
Manages the Tetris playfield: the cell grid, collision detection,
locking pieces in place, and detecting/clearing completed lines.
"""
from constants import BOARD_WIDTH, BOARD_HEIGHT
class Board:
    """The 10x20 Tetris playfield."""
    def __init__(self):
        """Create an empty board; each cell holds a color tuple or None."""
        self.grid = [[None for _ in range(BOARD_WIDTH)]
                     for _ in range(BOARD_HEIGHT)]
    def is_valid_position(self, tetromino, dx=0, dy=0, shape=None):
        """
        Return True if the tetromino, offset by (dx, dy) and optionally using
        an alternate shape matrix, lies entirely inside the board and does not
        overlap any locked cell.
        """
        for x, y in tetromino.get_cells(dx, dy, shape):
            if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT:
                return False
            if self.grid[y][x] is not None:
                return False
        return True
    def lock_piece(self, tetromino):
        """Permanently write the tetromino's cells into the grid."""
        for x, y in tetromino.get_cells():
            self.grid[y][x] = tetromino.color
    def clear_lines(self):
        """
        Remove every fully occupied row, shifting the rows above down.
        Return the number of rows cleared.
        """
        full_rows = [y for y in range(BOARD_HEIGHT)
                     if all(cell is not None for cell in self.grid[y])]
        for y in full_rows:
            del self.grid[y]
            self.grid.insert(0, [None for _ in range(BOARD_WIDTH)])
        return len(full_rows)
    def is_cell_filled(self, x, y):
        """Return True if the cell at (x, y) is occupied by a locked block."""
        return self.grid[y][x] is not None