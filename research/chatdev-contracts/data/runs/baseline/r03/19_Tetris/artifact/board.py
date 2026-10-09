'''
board.py
Defines the Board class: the 10x20 playfield grid, collision detection,
piece locking, line clearing and ghost-drop calculation.
'''
from constants import BOARD_WIDTH, BOARD_HEIGHT
class Board:
    def __init__(self):
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.grid = self._empty_grid()
    def _empty_grid(self):
        return [[None] * self.width for _ in range(self.height)]
    def reset(self):
        self.grid = self._empty_grid()
    def is_valid_position(self, piece, dx=0, dy=0, matrix=None):
        matrix = matrix if matrix is not None else piece.matrix
        for x, y in piece.cells(dx, dy, matrix):
            if x < 0 or x >= self.width or y >= self.height:
                return False
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True
    def lock_piece(self, piece):
        overflow = False
        for x, y in piece.cells():
            if y < 0:
                overflow = True
                continue
            self.grid[y][x] = piece.color
        return overflow
    def clear_lines(self):
        remaining = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = self.height - len(remaining)
        for _ in range(cleared):
            remaining.insert(0, [None] * self.width)
        self.grid = remaining
        return cleared
    def ghost_drop_distance(self, piece):
        distance = 0
        while self.is_valid_position(piece, dy=distance + 1):
            distance += 1
        return distance
    def is_game_over_on_spawn(self, piece):
        return not self.is_valid_position(piece)