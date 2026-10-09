'''
board.py
Defines the Board class: the 10x20 playfield grid.
Responsible for collision detection, locking pieces into the grid,
detecting and clearing completed lines, and determining whether the
stack has reached the top (game over condition).
'''
from constants import BOARD_WIDTH, BOARD_HEIGHT
class Board:
    """The Tetris playfield: a grid of colored cells or None."""
    def __init__(self, width=BOARD_WIDTH, height=BOARD_HEIGHT):
        self.width = width
        self.height = height
        self.grid = self._empty_grid()
    def _empty_grid(self):
        """Return a fresh grid filled with None (empty cells)."""
        return [[None for _ in range(self.width)] for _ in range(self.height)]
    def reset(self):
        """Clear the board back to its initial empty state."""
        self.grid = self._empty_grid()
    def is_inside(self, x, y):
        """True if the cell (x, y) lies within board boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height
    def is_valid_position(self, tetromino, x, y, matrix=None):
        """
        True if the tetromino placed at (x, y) fits entirely within the
        board and does not overlap any locked cell. Cells above the top
        of the board are allowed (pieces spawn partially off-screen).
        """
        if matrix is None:
            matrix = tetromino.matrix
        for cx, cy in tetromino.cells(x, y, matrix):
            if cx < 0 or cx >= self.width or cy >= self.height:
                return False
            if cy >= 0 and self.grid[cy][cx] is not None:
                return False
        return True
    def lock_piece(self, tetromino):
        """Write the tetromino's cells into the grid using its color."""
        for cx, cy in tetromino.cells():
            if 0 <= cy < self.height and 0 <= cx < self.width:
                self.grid[cy][cx] = tetromino.color
    def get_full_rows(self):
        """Return indices of rows that are completely filled."""
        return [row for row in range(self.height)
                if all(cell is not None for cell in self.grid[row])]
    def clear_lines(self):
        """
        Remove all completed rows, shifting everything above downward.
        Returns the number of rows cleared.
        """
        full_rows = self.get_full_rows()
        if not full_rows:
            return 0
        remaining = [row for row in self.grid
                     if not all(cell is not None for cell in row)]
        cleared = self.height - len(remaining)
        new_grid = [[None] * self.width for _ in range(cleared)]
        new_grid.extend(remaining)
        self.grid = new_grid
        return cleared
    def is_game_over(self, tetromino):
        """
        True if a freshly spawned tetromino cannot be placed anywhere,
        i.e. the spawn area is blocked by the stack.
        """
        return not self.is_valid_position(tetromino, tetromino.x, tetromino.y)
    def get_drop_y(self, tetromino):
        """Return the lowest valid y position for the tetromino (ghost)."""
        y = tetromino.y
        while self.is_valid_position(tetromino, tetromino.x, y + 1):
            y += 1
        return y