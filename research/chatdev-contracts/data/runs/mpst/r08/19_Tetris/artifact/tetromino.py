'''
tetromino.py
Defines the Tetromino class representing a single falling piece.
Each tetromino stores its shape matrix, color, and board position, and
provides rotation helpers (including wall-kick offset candidates) used by
the Game/Board modules to validate movement.
'''
import random
from constants import (
    SHAPE_MATRICES,
    SHAPE_COLORS,
    WALL_KICK_OFFSETS,
)
class Tetromino:
    """A single falling tetromino piece."""
    def __init__(self, shape_type=None):
        """
        Create a tetromino. If `shape_type` is None a random one of the
        seven standard shapes is chosen.
        """
        if shape_type is None:
            shape_type = random.choice(list(SHAPE_MATRICES.keys()))
        self.type = shape_type
        self.matrix = [row[:] for row in SHAPE_MATRICES[shape_type]]
        self.color = SHAPE_COLORS[shape_type]
        # Spawn position: horizontally centered, top of the board.
        self.x = 0
        self.y = 0
    @property
    def size(self):
        """Side length (rows/cols) of the piece's bounding matrix."""
        return len(self.matrix)
    def spawn_x(self, board_width):
        """Return the centered starting column for this piece."""
        return (board_width - self.size) // 2
    def rotated_matrix(self):
        """Return a new matrix rotated 90 degrees clockwise."""
        n = self.size
        return [[self.matrix[n - 1 - col][row] for col in range(n)]
                for row in range(n)]
    def rotation_offsets(self):
        """Candidate horizontal offsets for wall kicks after rotation."""
        return WALL_KICK_OFFSETS
    def cells(self, x=None, y=None, matrix=None):
        """
        Yield absolute board coordinates of occupied cells.
        Uses the piece's current position/matrix unless overrides given.
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        if matrix is None:
            matrix = self.matrix
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col]:
                    yield x + col, y + row