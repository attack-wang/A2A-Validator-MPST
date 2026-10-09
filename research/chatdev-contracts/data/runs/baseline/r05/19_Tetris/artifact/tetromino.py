'''
tetromino.py
Defines the Tetromino class: a single falling piece with its shape
matrix, board position, rotation helpers and cell enumeration.
'''
from constants import SHAPES, COLORS
class Tetromino:
    """A single tetromino with its shape matrix and board position."""
    def __init__(self, shape_type):
        self.type = shape_type
        self.matrix = [row[:] for row in SHAPES[shape_type]]
        self.x = 0
        self.y = 0
    @property
    def color(self):
        return COLORS[self.type]
    @property
    def size(self):
        return len(self.matrix)
    def cells(self):
        """Yield board coordinates (x, y) of every filled cell."""
        for r, row in enumerate(self.matrix):
            for c, val in enumerate(row):
                if val:
                    yield self.x + c, self.y + r
    def rotated_matrix(self, times=1):
        """Return a new matrix rotated `times` quarter-turns clockwise."""
        m = self.matrix
        for _ in range(times % 4):
            m = [list(t) for t in zip(*m[::-1])]
        return m
    def rotated_counterclockwise(self):
        """Return a new matrix rotated one quarter-turn counterclockwise."""
        return self.rotated_matrix(3)
    def get_spawn_position(self, board_width):
        """Center the piece horizontally at the top; returns (x, y)."""
        x = (board_width - len(self.matrix[0])) // 2
        y = 0
        for r, row in enumerate(self.matrix):
            if any(row):
                y = -r
                break
        return x, y