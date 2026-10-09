'''
piece.py
Defines the Piece class used to represent a single checker/draughts piece
on the board. A piece has a colour (RED or BLACK) and can be either a
regular "man" or a crowned "king".
'''
class Piece:
    '''Represents a single checkers piece (man or king).'''
    RED = 'red'
    BLACK = 'black'
    # Directions are (row_delta, col_delta) pairs on the 8x8 grid.
    # Row indices grow downward on the printed board (row 0 = rank 8).
    DOWN_RIGHT = (1, 1)
    DOWN_LEFT = (1, -1)
    UP_RIGHT = (-1, 1)
    UP_LEFT = (-1, -1)
    def __init__(self, color):
        if color not in (Piece.RED, Piece.BLACK):
            raise ValueError(f"Piece colour must be '{Piece.RED}' or '{Piece.BLACK}', got {color!r}.")
        self.color = color
        self.king = False
    def crown(self):
        '''Crown this piece, turning it into a king.'''
        self.king = True
    @property
    def is_king(self):
        return self.king
    @property
    def symbol(self):
        if self.color == Piece.RED:
            return 'R' if self.king else 'r'
        return 'B' if self.king else 'b'
    def direction(self):
        '''Row direction this piece's men move in. Kings move both ways.'''
        if self.king:
            return (Piece.DOWN_RIGHT, Piece.DOWN_LEFT, Piece.UP_RIGHT, Piece.UP_LEFT)
        if self.color == Piece.RED:
            # Red men start on rows 0-2 and march downward toward row 7.
            return (Piece.DOWN_RIGHT, Piece.DOWN_LEFT)
        # Black men start on rows 5-7 and march upward toward row 0.
        return (Piece.UP_RIGHT, Piece.UP_LEFT)
    def __repr__(self):
        return f"Piece('{self.color}', king={self.king})"
    def __str__(self):
        return self.symbol