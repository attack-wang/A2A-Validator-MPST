"""
tetromino.py
Defines the Tetromino piece and the 7-bag randomizer used to deal pieces
fairly, as in modern Tetris guidelines.
"""
import random
from constants import SHAPES, SHAPE_COLORS, BOARD_WIDTH
class Tetromino:
    """A single falling tetromino with position, shape matrix and color."""
    def __init__(self, shape_type):
        """
        Create a tetromino of the given type ('I', 'O', 'T', 'S', 'Z', 'J', 'L')
        positioned at the top-center of the board.
        """
        self.type = shape_type
        # Deep-copy the template so rotations never mutate the shared matrix.
        self.shape = [row[:] for row in SHAPES[shape_type]]
        self.color = SHAPE_COLORS[shape_type]
        # Center the piece horizontally at the top of the board.
        self.x = (BOARD_WIDTH - len(self.shape[0])) // 2
        self.y = 0
    def rotated_shape(self):
        """Return a new matrix with the shape rotated 90 degrees clockwise."""
        # Transpose + reverse rows == clockwise rotation.
        return [list(row) for row in zip(*self.shape[::-1])]
    def rotated_shape_ccw(self):
        """Return a new matrix with the shape rotated 90 degrees counter-clockwise."""
        # Reverse columns + transpose == counter-clockwise rotation.
        return [list(row) for row in zip(*self.shape)][::-1]
    def get_cells(self, dx=0, dy=0, shape=None):
        """
        Return the list of absolute board coordinates (x, y) occupied by the
        piece, optionally offset by (dx, dy) and/or using an alternate shape
        matrix (used to test rotations and moves before applying them).
        """
        if shape is None:
            shape = self.shape
        cells = []
        for row_index, row in enumerate(shape):
            for col_index, filled in enumerate(row):
                if filled:
                    cells.append((self.x + col_index + dx,
                                  self.y + row_index + dy))
        return cells
class PieceBag:
    """
    7-bag randomizer: all seven shapes are shuffled and dealt one by one;
    a new shuffled bag is created whenever the previous one is exhausted.
    This guarantees an even distribution of pieces over time.
    """
    def __init__(self):
        self.bag = []
    def next_type(self):
        """Return the next shape type, refilling and shuffling the bag if empty."""
        if not self.bag:
            self.bag = list(SHAPES.keys())
            random.shuffle(self.bag)
        return self.bag.pop()