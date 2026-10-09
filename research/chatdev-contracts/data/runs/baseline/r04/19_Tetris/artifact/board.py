'''
board.py
Board class managing the 10x20 grid: collision detection, locking pieces,
clearing completed lines, and game-over checks.
'''
from constants import BOARD_WIDTH, BOARD_HEIGHT
class Board:
    """The Tetris playfield: a grid of cells holding colors or None."""
    def __init__(self):
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.grid = self._create_empty_grid()
    def _create_empty_grid(self):
        return [[None for _ in range(self.width)] for _ in range(self.height)]
    def is_valid_position(self, tetromino, dx=0, dy=0, matrix=None):
        """Check whether the tetromino (moved by dx,dy, optionally with a new
        matrix) fits entirely inside the board without overlapping blocks."""
        if matrix is None:
            matrix = tetromino.matrix
        for cy, row in enumerate(matrix):
            for cx, cell in enumerate(row):
                if not cell:
                    continue
                x = tetromino.x + cx + dx
                y = tetromino.y + cy + dy
                if x < 0 or x >= self.width or y >= self.height:
                    return False
                if y >= 0 and self.grid[y][x] is not None:
                    return False
        return True
    def lock_tetromino(self, tetromino):
        """Write the tetromino's cells into the grid."""
        for y, x in tetromino.get_cells():
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x] = tetromino.color
    def clear_lines(self):
        """Remove all full rows, shifting rows above down.
        Returns the number of cleared lines."""
        cleared = 0
        new_grid = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = self.height - len(new_grid)
        while len(new_grid) < self.height:
            new_grid.insert(0, [None] * self.width)
        self.grid = new_grid
        return cleared
    def is_over_stack(self, tetromino):
        """Game over check: True if the freshly spawned tetromino collides
        immediately (no room to place it)."""
        return not self.is_valid_position(tetromino)