'''
board.py
Defines the Board class managing the 10x20 grid, collision detection,
piece locking, and line clearing.
'''
from constants import COLS, ROWS
class Board:
    """The playfield grid: tracks locked cells, validates moves, clears lines."""
    def __init__(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    def is_valid_position(self, matrix, piece_x, piece_y):
        """Check whether a piece matrix at (piece_x, piece_y) fits on the board."""
        for r, row in enumerate(matrix):
            for c, val in enumerate(row):
                if not val:
                    continue
                board_x = piece_x + c
                board_y = piece_y + r
                # Out of horizontal bounds or below bottom
                if board_x < 0 or board_x >= COLS or board_y >= ROWS:
                    return False
                # Above the top is allowed (pieces spawn there), but not overlapping
                if board_y >= 0 and self.grid[board_y][board_x] is not None:
                    return False
        return True
    def lock_piece(self, tetromino):
        """Write the tetromino's cells into the grid."""
        for (x, y) in tetromino.get_cells():
            if 0 <= y < ROWS and 0 <= x < COLS:
                self.grid[y][x] = tetromino.color
    def clear_lines(self):
        """Remove full rows, drop everything above, return number cleared."""
        full_rows = [r for r in range(ROWS) if all(cell is not None for cell in self.grid[r])]
        for r in full_rows:
            del self.grid[r]
            self.grid.insert(0, [None for _ in range(COLS)])
        return len(full_rows)
    def is_collision_at_spawn(self, tetromino):
        """Game over check: newly spawned piece overlaps existing blocks."""
        return not self.is_valid_position(tetromino.matrix, tetromino.x, tetromino.y)