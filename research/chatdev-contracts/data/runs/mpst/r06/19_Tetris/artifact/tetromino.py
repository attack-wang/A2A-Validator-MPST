'''
Tetromino module defining the seven standard Tetris pieces and their behavior.
'''
import random
from config import COLORS
SHAPES = {
    'I': [[0, 0, 0, 0],
          [1, 1, 1, 1],
          [0, 0, 0, 0],
          [0, 0, 0, 0]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1],
          [0, 0, 0]],
    'S': [[0, 1, 1],
          [1, 1, 0],
          [0, 0, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1],
          [0, 0, 0]],
    'J': [[1, 0, 0],
          [1, 1, 1],
          [0, 0, 0]],
    'L': [[0, 0, 1],
          [1, 1, 1],
          [0, 0, 0]],
}
class Tetromino:
    '''Represents a single falling tetromino piece.'''
    def __init__(self, shape_name=None, x=None, y=None):
        self.shape_name = shape_name if shape_name else random.choice(list(SHAPES.keys()))
        self.matrix = [row[:] for row in SHAPES[self.shape_name]]
        self.color = COLORS[self.shape_name]
        self.x = x if x is not None else 0
        self.y = y if y is not None else 0
    @property
    def width(self):
        return len(self.matrix[0])
    @property
    def height(self):
        return len(self.matrix)
    def top_offset(self):
        '''Number of empty rows at the top of the shape matrix.'''
        for row_idx, row in enumerate(self.matrix):
            if any(row):
                return row_idx
        return 0
    def rotated_matrix(self):
        '''Return the matrix rotated 90 degrees clockwise without modifying this piece.'''
        return [list(row) for row in zip(*self.matrix[::-1])]
    def rotate(self):
        '''Rotate the piece 90 degrees clockwise in place.'''
        self.matrix = self.rotated_matrix()
    def cells(self):
        '''Return list of (x, y) board coordinates occupied by this piece.'''
        result = []
        for row_idx, row in enumerate(self.matrix):
            for col_idx, val in enumerate(row):
                if val:
                    result.append((self.x + col_idx, self.y + row_idx))
        return result
    def spawn_position(self, board_width):
        '''Compute a centered spawn x offset for the given board width.'''
        return (board_width - self.width) // 2