'''
Rook piece: orthogonal slider.
'''
from piece import SlidingPiece
class Rook(SlidingPiece):
    letter = 'R'
    value = 5
    DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]