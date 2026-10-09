'''
tetromino.py
Defines the Tetromino piece (shape matrix, position, rotation, movement)
and a 7-bag randomizer that guarantees a fair distribution of all seven
standard tetromino shapes.
'''
import random
from constants import SHAPES, COLORS, BOARD_WIDTH
class Tetromino:
    """A single falling tetromino.
    The piece stores its shape as a square-ish matrix of 0/1 values, its
    top-left grid position (x, y) and the color associated with its type.
    """
    def __init__(self, shape_type):
        self.shape_type = shape_type
        self.color = COLORS[shape_type]
        self.matrix = [row[:] for row in SHAPES[shape_type]]
        # Spawn centered horizontally at the top of the board.
        self.x = (BOARD_WIDTH - len(self.matrix[0])) // 2
        self.y = 0
    def cells(self):
        """Return absolute board coordinates [(x, y), ...] of filled cells."""
        result = []
        for r, row in enumerate(self.matrix):
            for c, filled in enumerate(row):
                if filled:
                    result.append((self.x + c, self.y + r))
        return result
    def rotated_matrix(self):
        """Return the matrix rotated 90 degrees clockwise (without applying)."""
        return [list(row) for row in zip(*self.matrix[::-1])]
    def apply_matrix(self, matrix):
        self.matrix = matrix
    def move(self, dx, dy):
        """Shift the piece by (dx, dy) cells."""
        self.x += dx
        self.y += dy
    def width(self):
        return len(self.matrix[0])
    def height(self):
        return len(self.matrix)
class PieceBag:
    """7-bag randomizer.
    Shuffles all seven tetromino types and deals them one by one; when the
    bag is empty it is refilled and reshuffled. This guarantees that every
    shape appears regularly, as in modern Tetris games.
    """
    def __init__(self):
        self._bag = []
        self._refill()
    def _refill(self):
        self._bag = list(SHAPES.keys())
        random.shuffle(self._bag)
    def next_type(self):
        if not self._bag:
            self._refill()
        return self._bag.pop()