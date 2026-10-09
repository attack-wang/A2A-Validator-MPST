'''
board.py
Defines the Board class: the 10x20 playfield grid that tracks locked
cells, validates piece positions, locks pieces, clears completed lines
and detects the game-over condition.
'''
from constants import COLS, ROWS
class Board:
    """The Tetris playfield grid."""
    def __init__(self, cols=COLS, rows=ROWS):
        self.cols = cols
        self.rows = rows
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
    def is_valid_position(self, piece, dx=0, dy=0, shape=None):
        """Check whether the piece (optionally shifted/rotated) fits."""
        test_shape = shape if shape is not None else piece.shape
        for r, row in enumerate(test_shape):
            for c, val in enumerate(row):
                if not val:
                    continue
                x = piece.x + c + dx
                y = piece.y + r + dy
                # Outside horizontal bounds or below the floor
                if x < 0 or x >= self.cols or y >= self.rows:
                    return False
                # Above the top is allowed (pieces spawn there)
                if y < 0:
                    continue
                # Occupied by a locked cell
                if self.grid[y][x] is not None:
                    return False
        return True
    def lock_piece(self, piece):
        """Write the piece's cells into the grid. Returns True if any part of the piece is above the board (top-out)."""
        top_out = False
        for (x, y) in piece.get_cells():
            if y < 0:
                top_out = True
                continue
            self.grid[y][x] = piece.shape_type
        return top_out
    def clear_lines(self):
        """Remove full rows, drop everything above, return number cleared."""
        cleared = 0
        new_grid = []
        for row in self.grid:
            if all(cell is not None for cell in row):
                cleared += 1
            else:
                new_grid.append(row)
        for _ in range(cleared):
            new_grid.insert(0, [None] * self.cols)
        self.grid = new_grid
        return cleared
    def is_game_over(self, piece):
        """Game over when a newly spawned piece immediately collides."""
        return not self.is_valid_position(piece)