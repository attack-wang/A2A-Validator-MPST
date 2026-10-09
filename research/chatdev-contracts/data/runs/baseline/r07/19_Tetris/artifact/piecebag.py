# tetromino.py
import random
from settings import SHAPES, TETROMINO_COLORS
class Tetromino:
    def __init__(self, shape_key):
        self.shape_key = shape_key
        self.matrix = [row[:] for row in SHAPES[shape_key]]
        self.color = TETROMINO_COLORS[shape_key]
        self.x = 0
        self.y = 0
    @property
    def cells(self):
        """Return list of (x, y) board coordinates occupied by the piece."""
        ...
    def rotated_cw(self):
        """Return a new matrix rotated 90 degrees clockwise."""
        ...
    def rotated_ccw(self):
        ...
    def rotate_cw(self):
        self.matrix = self.rotated_cw()
    def rotate_ccw(self):
        self.matrix = self.rotated_ccw()
    def copy(self):
        ...
class PieceBag:
    """7-bag randomizer for fair piece distribution."""
    def __init__(self):
        self.bag = []
        self.refill()
    def refill(self):
        keys = list(SHAPES.keys())
        random.shuffle(keys)
        self.bag.extend(keys)
    def next(self):
        if not self.bag:
            self.refill()
        return self.bag.pop()