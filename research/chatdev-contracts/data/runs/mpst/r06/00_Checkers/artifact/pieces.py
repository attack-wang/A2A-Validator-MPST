'''
pieces.py
Piece model for checkers: player colors and individual pieces (men and kings).
'''
from enum import Enum
class PieceColor(Enum):
    '''The two players: Red moves first and advances toward row 8.'''
    RED = "red"
    BLACK = "black"
    @property
    def opposite(self):
        '''The other player's color.'''
        return PieceColor.BLACK if self is PieceColor.RED else PieceColor.RED
class Piece:
    '''A single checkers piece: a man, or a king after crowning.'''
    def __init__(self, color):
        self.color = color
        self.is_king = False
    def crown(self):
        '''Promote this man to a king (called when it reaches the king row).'''
        self.is_king = True
    @property
    def symbol(self):
        '''Board glyph: lowercase for men, uppercase for kings.'''
        if self.color == PieceColor.RED:
            return 'R' if self.is_king else 'r'
        return 'B' if self.is_king else 'b'