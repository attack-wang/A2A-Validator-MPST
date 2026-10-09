'''
pieces.py
Defines the Piece class and color constants used throughout the Checkers game.
A Piece tracks its color (RED or BLACK) and whether it has been crowned
as a King. Pieces render themselves as single-character symbols so the
board can be displayed in a terminal.
'''
RED = 'R'
BLACK = 'B'
MAN_SYMBOLS = {RED: 'r', BLACK: 'b'}
KING_SYMBOLS = {RED: 'R', BLACK: 'B'}
class Piece:
    '''Represents a single checker piece on the board.'''
    def __init__(self, color):
        if color not in (RED, BLACK):
            raise ValueError(f"Invalid color: {color!r}")
        self.color = color
        self.is_king = False
    def crown(self):
        self.is_king = True
    @property
    def symbol(self):
        return KING_SYMBOLS[self.color] if self.is_king else MAN_SYMBOLS[self.color]
    def __repr__(self):
        return f"Piece({self.color}, king={self.is_king})"