'''
board.py
The Board class manages the 10 x 20 playfield grid: collision detection,
locking pieces into the grid, detecting and clearing completed lines,
computing drop positions, and resetting for a new game.
'''
from constants import BOARD_WIDTH, BOARD_HEIGHT
class Board:
    '''The Tetris playfield: a grid whose cells hold a piece's color (or None).'''
    def __init__(self, width=BOARD_WIDTH, height=BOARD_HEIGHT):
        self.width = width
        self.height = height
        self.grid = self._make_grid()
    # -- setup -----------------------------------------------------------
    def _make_grid(self):
        '''Create a fresh empty grid (every cell is None).'''
        return [[None] * self.width for _ in range(self.height)]
    def reset(self):
        '''Clear the board for a new game.'''
        self.grid = self._make_grid()
    # -- queries ---------------------------------------------------------
    def is_valid_position(self, piece):
        '''True if every cell of `piece` lies inside the board and does not
        overlap an already locked cell. Cells above the top row (y < 0) are
        allowed so pieces can rotate while entering the field.'''
        for x, y in piece.cells():
            if x < 0 or x >= self.width or y >= self.height:
                return False
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True
    def is_game_over_state(self, piece):
        '''True if `piece` cannot be placed at its current position.'''
        return not self.is_valid_position(piece)
    def get_drop_distance(self, piece):
        '''Number of rows `piece` can fall before colliding (0 = already resting).'''
        distance = 0
        while self.is_valid_position(piece.moved(0, distance + 1)):
            distance += 1
        return distance
    def get_full_rows(self):
        '''Return the indices of completely filled rows.'''
        return [y for y in range(self.height) if all(self.grid[y])]
    # -- mutations -------------------------------------------------------
    def lock_piece(self, piece, color):
        '''Write `piece` into the grid using `color`.
        Returns False if any cell ended up above the top row (lock-out),
        which signals game over; otherwise True.'''
        above_top = False
        for x, y in piece.cells():
            if y < 0:
                above_top = True
                continue
            self.grid[y][x] = color
        return not above_top
    def clear_lines(self):
        '''Remove all full rows, shifting everything above down.
        Returns the number of rows cleared.'''
        full_rows = self.get_full_rows()
        if not full_rows:
            return 0
        full_set = set(full_rows)
        remaining = [row for y, row in enumerate(self.grid) if y not in full_set]
        empty_rows = [[None] * self.width for _ in range(len(full_rows))]
        self.grid = empty_rows + remaining
        return len(full_rows)