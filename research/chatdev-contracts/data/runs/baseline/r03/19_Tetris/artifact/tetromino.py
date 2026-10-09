'''
tetromino.py
Defines the Tetromino class (a single falling piece with shape, position and
rotation) and the BagRandomizer (7-bag piece generator for fair distribution).
'''
import random
from constants import SHAPES, SHAPE_COLORS, BOARD_WIDTH
class Tetromino:
    """A single falling Tetris piece."""
    def __init__(self, shape_type):
        if shape_type not in SHAPES:
            raise ValueError(f"Unknown tetromino type: {shape_type}")
        self.shape_type = shape_type
        self.matrix = [row[:] for row in SHAPES[shape_type]]
        self.color = SHAPE_COLORS[shape_type]
        self.x = 0
        self.y = 0
        self._reset_spawn_position()
    def _reset_spawn_position(self):
        self.x = (BOARD_WIDTH - len(self.matrix[0])) // 2
        first_filled_row = 0
        for index, row in enumerate(self.matrix):
            if any(row):
                first_filled_row = index
                break
        self.y = -first_filled_row
    def cells(self, dx=0, dy=0, matrix=None):
        matrix = matrix if matrix is not None else self.matrix
        return [(self.x + c + dx, self.y + r + dy)
                for r, row in enumerate(matrix) for c, val in enumerate(row) if val]
    def rotated_matrix(self, direction):
        if direction == 1:
            return [list(row) for row in zip(*self.matrix[::-1])]
        return [list(row) for row in zip(*self.matrix)][::-1]
    def rotate(self, direction):
        self.matrix = self.rotated_matrix(direction)
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    def copy(self):
        clone = Tetromino(self.shape_type)
        clone.matrix = [row[:] for row in self.matrix]
        clone.x = self.x
        clone.y = self.y
        return clone
class BagRandomizer:
    """7-bag randomizer."""
    def __init__(self):
        self._bag = []
        self.next_type = self._draw_from_bag()
    def _draw_from_bag(self):
        if not self._bag:
            self._bag = list(SHAPES.keys())
            random.shuffle(self._bag)
        return self._bag.pop()
    def take_next_type(self):
        current = self.next_type
        self.next_type = self._draw_from_bag()
        return current