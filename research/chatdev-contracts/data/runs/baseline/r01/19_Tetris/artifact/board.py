'''
board.py
Defines the Board class: the 10x20 playfield grid with collision
detection, piece locking, completed-line clearing and reset support.
'''
from constants import BOARD_WIDTH, BOARD_HEIGHT
class Board:
    """The Tetris playfield: a grid whose cells hold a color or None."""
    def __init__(self):
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.grid = []
        self.reset()
    def reset(self):
        """Empty every cell of the grid."""
        self.grid = [[None] * self.width for _ in range(self.height)]
    def is_inside(self, col, row):
        """True if (col, row) lies within the horizontal bounds; rows above
        the top edge are tolerated so pieces can rotate at the very top."""
        return 0 <= col < self.width and row < self.height
    def is_valid_position(self, tetromino, dx=0, dy=0, matrix=None):
        """True if the piece, shifted by (dx, dy) and using `matrix`,
        fits inside the board without overlapping locked cells."""
        if matrix is None:
            matrix = tetromino.matrix
        for col, row in tetromino.get_cells(matrix, tetromino.x + dx, tetromino.y + dy):
            if not self.is_inside(col, row):
                return False
            if row >= 0 and self.grid[row][col] is not None:
                return False
        return True
    def lock_tetromino(self, tetromino):
        """Merge the piece into the grid.
        Returns False if any cell locked above the top edge (lock out),
        which signals a game over; otherwise returns True.
        """
        for col, row in tetromino.get_cells():
            if row < 0:
                return False
            self.grid[row][col] = tetromino.color
        return True
    def get_full_rows(self):
        """Return the indices of completely filled rows."""
        return [row for row in range(self.height)
                if all(cell is not None for cell in self.grid[row])]
    def clear_lines(self):
        """Delete full rows and shift the rows above down.
        Returns the number of cleared lines.
        """
        full_rows = self.get_full_rows()
        for row in full_rows:
            del self.grid[row]
            self.grid.insert(0, [None] * self.width)
        return len(full_rows)
    def is_empty_cell(self, col, row):
        """True if the cell is inside the board and not locked."""
        return self.is_inside(col, row) and (row < 0 or self.grid[row][col] is None)