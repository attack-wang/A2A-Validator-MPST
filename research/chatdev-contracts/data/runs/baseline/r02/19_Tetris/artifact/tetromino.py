'''
tetromino.py
Tetromino: one falling piece (type, color, rotation, position) plus the
rotate_matrix helper used to derive orientation matrices.
'''
import random
from constants import COLS, SHAPES, SHAPE_COLORS
def rotate_matrix(matrix, times=1):
    '''Return a NEW matrix rotated 90 degrees clockwise `times` times.'''
    times %= 4
    result = [row[:] for row in matrix]
    for _ in range(times):
        result = [list(row) for row in zip(*result[::-1])]
    return result
class Tetromino:
    '''A single tetromino; its matrix is derived from SHAPES + rotation.'''
    def __init__(self, shape_type=None):
        '''Pick a random shape if none given; center horizontally at the top.'''
        self.type = shape_type if shape_type in SHAPES else random.choice(list(SHAPES.keys()))
        self.color = SHAPE_COLORS[self.type]
        self.rotation = 0
        self.x = (COLS - len(SHAPES[self.type][0])) // 2
        self.y = 0
    @property
    def matrix(self):
        '''Current orientation matrix derived from the base shape + rotation.'''
        return rotate_matrix(SHAPES[self.type], self.rotation)
    def cells(self, matrix=None, x=None, y=None):
        '''Absolute board coordinates of every filled cell of this piece.'''
        matrix = self.matrix if matrix is None else matrix
        x = self.x if x is None else x
        y = self.y if y is None else y
        return [(x + cx, y + cy)
                for cy, row in enumerate(matrix)
                for cx, val in enumerate(row) if val]
    def rotated_matrix(self):
        '''Matrix that would result from one clockwise rotation.'''
        return rotate_matrix(SHAPES[self.type], (self.rotation + 1) % 4)