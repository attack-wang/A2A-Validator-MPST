'''
Bishop piece: diagonal slider.
'''
from piece import SlidingPiece
class Bishop(SlidingPiece):
    letter = 'B'
    value = 3
    DIRECTIONS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]