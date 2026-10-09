'''
Board module managing the Tetris playfield: locking pieces, collision checks and line clears.
'''
from config import BOARD_WIDTH, BOARD_HEIGHT
class Board:
    '''Represents the 10x20 Tetris playfield.'''
    def __init__(self, width=BOARD_WIDTH, height=BOARD_HEIGHT):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
    def is_inside(self, x, y):
        '''Return True if the coordinates lie within the board boundaries.'''
        return 0 <= x < self.width and 0 <= y < self.height
    def is_free(self, x, y):
        '''A cell is free if it is inside the board and not occupied.'''
        if x < 0 or x >= self.width or y >= self.height:
            return False
        if y < 0:
            return True  # allow pieces above the board during spawn/rotation
        return self.grid[y][x] is None
    def can_place(self, tetromino, dx=0, dy=0, matrix=None):
        '''Check whether the tetromino (optionally moved/rotated) fits without collision.'''
        m = matrix if matrix is not None else tetromino.matrix
        for row_idx, row in enumerate(m):
            for col_idx, val in enumerate(row):
                if val:
                    x = tetromino.x + col_idx + dx
                    y = tetromino.y + row_idx + dy
                    if not self.is_free(x, y):
                        return False
        return True
    def lock(self, tetromino):
        '''Merge the tetromino into the grid. Returns False if any cell is above the top.'''
        for x, y in tetromino.cells():
            if y < 0:
                return False
            self.grid[y][x] = tetromino.color
        return True
    def clear_lines(self):
        '''Remove completed rows, shifting everything above down. Returns number of cleared lines.'''
        remaining = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = self.height - len(remaining)
        for _ in range(cleared):
            remaining.insert(0, [None for _ in range(self.width)])
        self.grid = remaining
        return cleared