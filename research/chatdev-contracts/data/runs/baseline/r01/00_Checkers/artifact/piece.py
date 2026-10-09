'''
piece.py
Defines the Piece class representing a single checkers piece (man or king),
including color constants and the symbol used for board rendering.
'''
RED = 'red'
BLACK = 'black'
class Piece:
    def __init__(self, color):
        if color not in (RED, BLACK):
            raise ValueError(f"Invalid piece color: {color!r}")
        self.color = color
        self.is_king = False
    def promote(self):
        self.is_king = True
    def copy(self):
        clone = Piece(self.color)
        clone.is_king = self.is_king
        return clone
    @property
    def symbol(self):
        if self.color == RED:
            return 'R' if self.is_king else 'r'
        return 'B' if self.is_king else 'b'
    def __repr__(self):
        return f"Piece({self.color}, {'king' if self.is_king else 'man'})"