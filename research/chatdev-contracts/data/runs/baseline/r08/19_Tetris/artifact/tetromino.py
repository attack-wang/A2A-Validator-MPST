'''
tetromino.py
Defines the seven standard Tetris tetromino shapes (I, O, T, S, Z, J, L),
matrix rotation helpers, and the Tetromino class that tracks a piece's
type, rotation state, and board position.
'''
import random
# Each shape is a matrix of 0/1; all four rotation states are pre-computed
# per piece so rotation is a simple index change.
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]],
}
SHAPE_TYPES = list(SHAPES.keys())
def rotate_matrix(matrix, times=1):
    '''Return a copy of `matrix` rotated clockwise `times` times (90° per step).'''
    result = [row[:] for row in matrix]
    for _ in range(times % 4):
        result = [list(row) for row in zip(*result[::-1])]
    return result
class Tetromino:
    '''A single falling tetromino with type, rotation index, and (x, y) position.
    x and y refer to the top-left corner of the piece's bounding matrix on
    the board grid; y may be negative while a piece is still entering.
    '''
    def __init__(self, shape_type, x=0, y=0, rotation=0):
        if shape_type not in SHAPES:
            raise ValueError(f'Unknown tetromino type: {shape_type}')
        self.type = shape_type
        self.x = x
        self.y = y
        self.rotation = rotation % 4
        # Pre-compute the four rotation states of this shape.
        states = [SHAPES[shape_type]]
        for _ in range(3):
            states.append(rotate_matrix(states[-1]))
        self._rotation_states = states
    @property
    def shape(self):
        '''Current 2D matrix describing the piece's occupied cells.'''
        return self._rotation_states[self.rotation]
    @property
    def width(self):
        return len(self.shape[0])
    @property
    def height(self):
        return len(self.shape)
    def cells(self):
        '''Return the list of absolute board coordinates (x, y) the piece fills.'''
        return [(self.x + col, self.y + row)
                for row, line in enumerate(self.shape)
                for col, filled in enumerate(line) if filled]
    def moved(self, dx, dy):
        '''Return an identical piece translated by (dx, dy).'''
        return Tetromino(self.type, self.x + dx, self.y + dy, self.rotation)
    def rotated(self, direction=1):
        '''Return an identical piece with rotation shifted by `direction`
        (+1 = clockwise, -1 = counter-clockwise).'''
        return Tetromino(self.type, self.x, self.y, (self.rotation + direction) % 4)
    def copy(self):
        return Tetromino(self.type, self.x, self.y, self.rotation)
def random_tetromino(x=0, y=0):
    '''Factory returning a Tetromino of a uniformly random type.'''
    return Tetromino(random.choice(SHAPE_TYPES), x, y)