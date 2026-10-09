'''
tetromino.py
Defines the Tetromino class representing a falling piece.
'''
import random
from constants import SHAPES, COLORS, BOARD_WIDTH
class Tetromino:
    """A single falling Tetris piece with shape, color, position and rotation."""
    def __init__(self, shape_type=None):
        self.shape_type = shape_type if shape_type else random.choice(list(SHAPES.keys()))
        self.matrix = [row[:] for row in SHAPES[self.shape_type]]
        self.color = COLORS[self.shape_type]
        # Spawn position: centered horizontally, at the top of the board
        self.x = (BOARD_WIDTH - len(self.matrix[0])) // 2
        self.y = 0  # could use -offset for pieces with empty top rows
    def get_cells(self):
        """Return list of (x, y) board coordinates occupied by this piece."""
        cells = []
        for row_idx, row in enumerate(self.matrix):
            for col_idx, val in enumerate(row):
                if val:
                    cells.append((self.x + col_idx, self.y + row_idx))
        return cells
    def rotated_matrix(self):
        """Return the matrix rotated 90 degrees clockwise without mutating state."""
        return [list(row) for row in zip(*self.matrix[::-1])]
    def rotate(self):
        """Rotate the piece clockwise in place."""
        self.matrix = self.rotated_matrix()
    def move(self, dx, dy):
        """Move the piece by (dx, dy) cells."""
        self.x += dx
        self.y += dy
    def copy(self):
        """Return a deep copy of this tetromino."""
        new = Tetromino(self.shape_type)
        new.matrix = [row[:] for row in self.matrix]
        new.x = self.x
        new.y = self.y
        return new