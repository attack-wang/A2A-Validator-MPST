'''
Queen piece: combined rook + bishop slider.
'''
from bishop import Bishop
from rook import Rook
from piece import SlidingPiece
class Queen(SlidingPiece):
    letter = 'Q'
    value = 9
    DIRECTIONS = Bishop.DIRECTIONS + Rook.DIRECTIONS