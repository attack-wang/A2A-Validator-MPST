'''
tetromino.py
Defines the seven standard Tetris tetromino shapes (I, O, T, S, Z, J, L)
and the Tetromino class supporting rotation, positioning, and cell lookup.
'''
import random
from constants import BOARD_WIDTH, COLORS
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[1, 1, 1],
          [0, 1, 0]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]],
}
SHAPE_TYPES = list(SHAPES.keys())
class Tetromino:
    """One falling tetromino: shape matrix, color, and board position."""
    def __init__(self, shape_type=None):
        if shape_type is None:
            shape_type = random.choice(SHAPE_TYPES)
        self.type = shape_type
        self.matrix = [row[:] for row in SHAPES[shape_type]]
        self.color = COLORS[shape_type]
        self.x = (BOARD_WIDTH - len(self.matrix[0])) // 2
        self.y = 0
    def rotated_matrix(self):
        """Return a new matrix rotated 90 degrees clockwise (state unchanged)."""
        return [list(row) for row in zip(*self.matrix[::-1])]
    def apply_rotation(self, matrix):
        """Replace the current matrix with a pre-rotated one."""
        self.matrix = matrix
    def get_cells(self, dx=0, dy=0):
        """Absolute board coordinates (x, y) of occupied cells, with offset."""
        return [
            (self.x + cx + dx, self.y + cy + dy)
            for cy, row in enumerate(self.matrix)
            for cx, cell in enumerate(row)
            if cell
        ]
    def copy(self):
        """Return an independent copy of this tetromino."""
        clone = Tetromino(self.type)
        clone.matrix = [row[:] for row in self.matrix]
        clone.x = self.x
        clone.y = self.y
        return clone