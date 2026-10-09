'''
tetromino.py
Defines the Tetromino class representing the seven standard falling
pieces (I, O, T, S, Z, J, L), including their shape matrices, colors,
rotation logic and movement helpers.
'''
import random
from constants import TETROMINO_COLORS
class Tetromino:
    """A single falling tetromino piece."""
    # Shape matrices: 1 marks an occupied cell, 0 an empty one.
    SHAPES = {
        'I': [[0, 0, 0, 0],
              [1, 1, 1, 1],
              [0, 0, 0, 0],
              [0, 0, 0, 0]],
        'O': [[1, 1],
              [1, 1]],
        'T': [[0, 1, 0],
              [1, 1, 1],
              [0, 0, 0]],
        'S': [[0, 1, 1],
              [1, 1, 0],
              [0, 0, 0]],
        'Z': [[1, 1, 0],
              [0, 1, 1],
              [0, 0, 0]],
        'J': [[1, 0, 0],
              [1, 1, 1],
              [0, 0, 0]],
        'L': [[0, 0, 1],
              [1, 1, 1],
              [0, 0, 0]],
    }
    def __init__(self, shape_type=None):
        self.shape_type = shape_type if shape_type else random.choice(list(self.SHAPES.keys()))
        self.shape = [row[:] for row in self.SHAPES[self.shape_type]]
        self.color = TETROMINO_COLORS[self.shape_type]
        # Spawn near the top-center of the board
        self.x = 0
        self.y = 0
    def get_cells(self):
        """Return absolute board coordinates of occupied cells."""
        cells = []
        for r, row in enumerate(self.shape):
            for c, val in enumerate(row):
                if val:
                    cells.append((self.x + c, self.y + r))
        return cells
    def rotated_shape(self):
        """Return the shape matrix rotated 90 degrees clockwise."""
        return [list(row) for row in zip(*self.shape[::-1])]
    def rotate(self):
        """Rotate the piece clockwise in place."""
        self.shape = self.rotated_shape()
    def move(self, dx, dy):
        """Shift the piece by (dx, dy) cells."""
        self.x += dx
        self.y += dy
    def set_position(self, x, y):
        self.x = x
        self.y = y