'''
board.py
Defines the Board class managing the playfield grid, collisions and line clears.
'''
from constants import BOARD_WIDTH, BOARD_HEIGHT
class Board:
    """Represents the Tetris playfield: a grid of locked cells."""
    def __init__(self):
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.reset()
    def reset(self):
        """Clear the grid to an empty state."""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    def is_inside(self, x, y):
        """Check whether a cell coordinate lies within board bounds."""
        return 0 <= x < self.width and 0 <= y < self.height
    def is_valid_position(self, tetromino, dx=0, dy=0, matrix=None):
        """Check whether the tetromino (optionally moved/rotated) fits on the board."""
        if matrix is None:
            matrix = tetromino.matrix
        for row_idx, row in enumerate(matrix):
            for col_idx, val in enumerate(row):
                if not val:
                    continue
                x = tetromino.x + col_idx + dx
                y = tetromino.y + row_idx + dy
                if not self.is_inside(x, y):
                    return False
                if y >= 0 and self.grid[y][x] is not None:
                    return False
        return True
    def lock_piece(self, tetromino):
        """Write the tetromino cells into the grid using its color.
        Returns True if any part of the piece locked above the board
        (standard 'lock out' game-over condition).
        """
        lock_out = False
        for x, y in tetromino.get_cells():
            if y < 0:
                lock_out = True
                continue
            self.grid[y][x] = tetromino.color
        return lock_out
    def clear_lines(self):
        """Remove completed rows, shift rows above down; return number of cleared lines."""
        cleared = 0
        new_grid = []
        for row in self.grid:
            if all(cell is not None for cell in row):
                cleared += 1
            else:
                new_grid.append(row)
        for _ in range(cleared):
            new_grid.insert(0, [None for _ in range(self.width)])
        self.grid = new_grid
        return cleared
    def is_game_over(self, tetromino):
        """True when a freshly spawned tetromino overlaps locked cells."""
        return not self.is_valid_position(tetromino)