'''
board.py
The playfield: a ROWS x COLS grid that stores locked cells, validates
piece positions, merges landed pieces and clears completed lines.
'''
from settings import COLS, ROWS
class Board:
    """Grid of locked cells plus collision / line-clearing logic."""
    def __init__(self):
        self.grid = self._empty_grid()
    @staticmethod
    def _empty_grid():
        return [[None] * COLS for _ in range(ROWS)]
    def reset(self):
        self.grid = self._empty_grid()
    def is_inside(self, x, y):
        return 0 <= x < COLS and 0 <= y < ROWS
    def cell_free(self, x, y):
        return self.is_inside(x, y) and self.grid[y][x] is None
    def is_valid_position(self, piece, dx=0, dy=0, matrix=None):
        """True if the piece (shifted by dx/dy, optionally using another
        matrix) fits entirely inside the board without overlapping locked
        cells. Cells above the top (y < 0) are allowed so pieces can spawn
        and rotate partially outside the visible playfield.
        """
        for x, y in piece.cells(dx, dy, matrix):
            if x < 0 or x >= COLS or y >= ROWS:
                return False
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True
    def lock_piece(self, piece):
        """Merge the piece into the grid.
        Returns True if any cell ended up above the visible playfield,
        which means the stack has overflowed (game over).
        """
        overflow = False
        for x, y in piece.cells():
            if 0 <= y < ROWS and 0 <= x < COLS:
                self.grid[y][x] = piece.shape_key
            elif y < 0:
                overflow = True
        return overflow
    def full_rows(self):
        """Indices of completely filled rows."""
        return [y for y in range(ROWS)
                if all(cell is not None for cell in self.grid[y])]
    def clear_rows(self, rows):
        """Remove the given rows and drop everything above them down."""
        for y in sorted(rows, reverse=True):
            del self.grid[y]
        for _ in rows:
            self.grid.insert(0, [None] * COLS)