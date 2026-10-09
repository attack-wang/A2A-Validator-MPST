'''
tetromino.py
Defines the Tetromino piece and the 7-bag randomizer.
Tetromino stores the shape matrix, its colour key and its position on the
board, and provides rotation helpers that return rotated copies of the
matrix (used by the wall-kick logic in the Game class).
PieceBag implements the standard "7-bag" randomizer: all seven shapes are
shuffled and dealt one by one, guaranteeing an even distribution of pieces
over time.
'''
import random
from settings import SHAPES, TETROMINO_COLORS
class Tetromino:
    """A single falling tetromino (shape, colour, rotation and position)."""
    def __init__(self, shape_key):
        self.shape_key = shape_key
        # Deep copy so rotations never mutate the shared SHAPES templates.
        self.matrix = [row[:] for row in SHAPES[shape_key]]
        self.color = TETROMINO_COLORS[shape_key]
        self.x = 0  # column of the matrix' top-left corner on the board
        self.y = 0  # row of the matrix' top-left corner on the board
    @property
    def width(self):
        return len(self.matrix[0])
    @property
    def height(self):
        return len(self.matrix)
    def cells(self, dx=0, dy=0, matrix=None):
        """Board coordinates (x, y) of every filled cell of the piece.
        Optional dx/dy offsets and an alternative matrix (e.g. a rotated
        copy) let the Board test hypothetical positions for movement and
        wall kicks without mutating the piece.
        """
        m = self.matrix if matrix is None else matrix
        result = []
        for r, row in enumerate(m):
            for c, filled in enumerate(row):
                if filled:
                    result.append((self.x + c + dx, self.y + r + dy))
        return result
    def rotated_cw(self):
        """Return a new matrix rotated 90 degrees clockwise."""
        return [list(row) for row in zip(*self.matrix[::-1])]
    def rotated_ccw(self):
        """Return a new matrix rotated 90 degrees counter-clockwise."""
        return [list(row) for row in zip(*self.matrix)][::-1]
    def rotate_cw(self):
        self.matrix = self.rotated_cw()
    def rotate_ccw(self):
        self.matrix = self.rotated_ccw()
class PieceBag:
    """7-bag randomizer: deals each of the seven shapes once per shuffle."""
    def __init__(self):
        self._bag = []
        self._refill()
    def _refill(self):
        keys = list(SHAPES.keys())
        random.shuffle(keys)
        self._bag.extend(keys)
    def next(self):
        """Pop the next shape key, refilling the bag when it runs empty."""
        if not self._bag:
            self._refill()
        return self._bag.pop()