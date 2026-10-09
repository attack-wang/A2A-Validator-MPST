'''
board.py
Board: 10x20 grid, collision detection, locking pieces, clearing lines.
'''
from constants import COLS, ROWS
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    def is_valid_position(self, matrix, x, y):
        '''True if the piece matrix can be placed at (x, y) without
        colliding with walls, floor or locked cells.'''
        for cy, row in enumerate(matrix):
            for cx, val in enumerate(row):
                if not val:
                    continue
                bx, by = x + cx, y + cy
                if bx < 0 or bx >= COLS or by >= ROWS:
                    return False
                if by >= 0 and self.grid[by][bx] is not None:
                    return False
        return True
    def lock_piece(self, tetromino):
        '''Write the piece's cells into the grid. Returns True if any part
        of the piece ended up above the visible board (top-out).'''
        top_out = False
        for bx, by in tetromino.cells():
            if by < 0:
                top_out = True
                continue
            self.grid[by][bx] = tetromino.color
        return top_out
    def clear_lines(self):
        '''Remove all full rows. Returns number of cleared lines.'''
        full_rows = [r for r in range(ROWS) if all(self.grid[r])]
        for r in full_rows:
            del self.grid[r]
            self.grid.insert(0, [None for _ in range(COLS)])
        return len(full_rows)
    def is_collision_at_spawn(self, tetromino):
        '''True if a freshly spawned piece overlaps locked cells or walls,
        i.e. the game cannot continue (board is too full).'''
        return not self.is_valid_position(tetromino.matrix,
                                          tetromino.x, tetromino.y)