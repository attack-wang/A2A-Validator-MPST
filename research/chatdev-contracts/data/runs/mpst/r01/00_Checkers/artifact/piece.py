'''
piece.py
Defines the Piece class representing a single checkers piece.
'''
class Piece:
    '''Represents a checkers piece (man or king) belonging to a player.'''
    def __init__(self, color):
        '''Create a man of the given color ("red" or "black"); not a king yet.'''
        self.color = color
        self.is_king = False
    def crown(self):
        '''Promote this piece to a king.'''
        self.is_king = True
    @property
    def symbol(self):
        '''One-character board symbol: lowercase for men, uppercase for kings.'''
        if self.is_king:
            return 'R' if self.color == 'red' else 'B'
        return 'r' if self.color == 'red' else 'b'
    def __repr__(self):
        '''Developer-friendly representation of the piece.'''
        return f"Piece({self.color}, {'king' if self.is_king else 'man'})"