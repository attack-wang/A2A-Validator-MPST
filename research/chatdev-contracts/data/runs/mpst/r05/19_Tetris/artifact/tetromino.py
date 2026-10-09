'''
tetromino.py
Defines the Tetromino class representing a falling piece, including all
seven standard shapes, rotation logic, and position management.
'''
import random
from constants import SHAPES, COLORS, COLS
class Tetromino:
    """A single falling tetromino piece with shape, color, position, and rotation."""
    SHAPE_TYPES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
    def __init__(self, shape_type=None):
        """Create a tetromino of the given type (or random) at its spawn position."""
        self.shape_type = shape_type if shape_type else random.choice(self.SHAPE_TYPES)
        self.matrix = [row[:] for row in SHAPES[self.shape_type]]
        self.color = COLORS[self.shape_type]
        # Spawn position: centered horizontally, at the top of the board.
        # Use the matrix width so each shape centers correctly:
        # 'I' (4 cols) -> x = 3, 'O' (2 cols) -> x = 4, 3-wide shapes -> x = 3.
        self.x = (COLS - len(self.matrix[0])) // 2
        self.y = 0
    def rotate(self):
        """Return a new matrix rotated 90 degrees clockwise."""
        rows = len(self.matrix)
        cols = len(self.matrix[0])
        return [[self.matrix[rows - 1 - c][r] for c in range(rows)] for r in range(cols)]
    def apply_rotation(self):
        """Replace the current matrix with its clockwise-rotated version."""
        self.matrix = self.rotate()
    def get_cells(self):
        """Return list of (x, y) board coordinates occupied by this piece."""
        cells = []
        for r, row in enumerate(self.matrix):
            for c, val in enumerate(row):
                if val:
                    cells.append((self.x + c, self.y + r))
        return cells