'''
tetromino.py
Defines the Tetromino class: a single falling piece.
A tetromino stores its shape as a 2D matrix, a grid position (col, row)
and a color. It supports clockwise rotation (with matrix transformation)
and can report the absolute board coordinates of its occupied cells.
'''
import random
from settings import SHAPES, SHAPE_COLORS, COLS
class Tetromino:
    """One falling tetromino piece."""
    def __init__(self, shape_name=None, col=None, row=0):
        """
        Create a tetromino. If `shape_name` is omitted a random one of the
        seven standard shapes is chosen.
        """
        self.shape_name = shape_name if shape_name else random.choice(list(SHAPES.keys()))
        self.matrix = [row[:] for row in SHAPES[self.shape_name]]
        self.color = SHAPE_COLORS[self.shape_name]
        self.col = col if col is not None else self.spawn_col()
        self.row = row
    def spawn_col(self):
        """Horizontally center the piece on the board."""
        return (COLS - len(self.matrix[0])) // 2
    @property
    def width(self):
        return len(self.matrix[0])
    @property
    def height(self):
        return len(self.matrix)
    def rotated_matrix(self):
        """Return the matrix rotated 90 degrees clockwise (without applying)."""
        return [list(r) for r in zip(*self.matrix[::-1])]
    def rotate(self):
        """Apply a clockwise rotation to the piece matrix."""
        self.matrix = self.rotated_matrix()
    def cells(self, dx=0, dy=0, matrix=None):
        """
        Return the absolute board coordinates of every occupied cell,
        optionally offset by (dx, dy) and/or using an alternative matrix
        (used to test rotations and moves before committing them).
        """
        if matrix is None:
            matrix = self.matrix
        result = []
        for r, row in enumerate(matrix):
            for c, val in enumerate(row):
                if val:
                    result.append((self.col + c + dx, self.row + r + dy))
        return result
    def copy(self):
        """Return an independent copy of this piece."""
        new = Tetromino(self.shape_name, self.col, self.row)
        new.matrix = [row[:] for row in self.matrix]
        return new