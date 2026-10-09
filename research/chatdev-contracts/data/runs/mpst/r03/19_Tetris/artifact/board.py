'''
board.py
Defines the Board class: the 10x20 grid that stores locked cells, performs
collision detection, locks pieces in place, and clears completed lines.
'''
from constants import BOARD_WIDTH, BOARD_HEIGHT
class Board:
    """Grid-based playfield with collision detection and line clearing."""
    def __init__(self):
        self.grid = [[None] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    def is_valid_position(self, tetromino, dx=0, dy=0, matrix=None):
        """True if the piece (optionally offset/rotated) fits inside the
        board and does not overlap locked cells."""
        if matrix is None:
            matrix = tetromino.matrix
        for r, row in enumerate(matrix):
            for c, filled in enumerate(row):
                if not filled:
                    continue
                x = tetromino.x + c + dx
                y = tetromino.y + r + dy
                # Outside horizontal bounds or below the floor.
                if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                    return False
                # Above the visible top is allowed (spawn area), but any
                # overlap with locked cells is a collision.
                if y >= 0 and self.grid[y][x] is not None:
                    return False
        return True
    def lock_piece(self, tetromino):
        """Write the piece's cells into the grid.
        Returns True if any block ended up above the visible board (which
        means the stack has overflowed and the game is over).
        """
        overflow = False
        for x, y in tetromino.cells():
            if y < 0:
                overflow = True
                continue
            self.grid[y][x] = tetromino.color
        return overflow
    def clear_lines(self):
        """Remove all completed rows.
        Returns the number of rows cleared.
        """
        full_rows = [y for y in range(BOARD_HEIGHT) if all(self.grid[y])]
        for y in full_rows:
            del self.grid[y]
            self.grid.insert(0, [None] * BOARD_WIDTH)
        return len(full_rows)
    def is_cell_filled(self, x, y):
        return self.grid[y][x] is not None