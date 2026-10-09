'''
Defines the Tetromino class: a single falling piece built from one of the
seven standard shapes, supporting rotation and cell-position queries.
'''
import random
from constants import SHAPES, TETROMINO_COLORS, BOARD_COLS
class Tetromino:
    """A falling tetromino piece with a shape matrix, color and board position."""
    def __init__(self, shape_type=None):
        """
        Create a tetromino. If `shape_type` is omitted, a random one of the
        seven standard shapes is chosen.
        """
        if shape_type is None:
            shape_type = random.choice(list(SHAPES.keys()))
        self.shape_type = shape_type
        # Work on a copy so the shared SHAPES template is never mutated.
        self.matrix = [row[:] for row in SHAPES[shape_type]]
        self.color = TETROMINO_COLORS[shape_type]
        # Spawn horizontally centered on the top row of the board.
        self.x = (BOARD_COLS - len(self.matrix[0])) // 2
        self.y = 0
    def rotated_matrix(self):
        """Return the shape matrix rotated 90 degrees clockwise."""
        return [list(row) for row in zip(*self.matrix[::-1])]
    def apply_matrix(self, matrix):
        """Replace the current shape matrix (used after a successful rotation)."""
        self.matrix = matrix
    def get_cells(self, dx=0, dy=0, matrix=None):
        """
        Return the list of absolute board coordinates (x, y) occupied by the
        piece, optionally translated by (dx, dy) and/or using an alternative
        (rotated) matrix. Used for collision checks before applying a move.
        """
        if matrix is None:
            matrix = self.matrix
        cells = []
        for row_idx, row in enumerate(matrix):
            for col_idx, value in enumerate(row):
                if value:
                    cells.append((self.x + col_idx + dx, self.y + row_idx + dy))
        return cells