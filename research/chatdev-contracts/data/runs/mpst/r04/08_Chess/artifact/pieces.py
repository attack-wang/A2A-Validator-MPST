'''
pieces.py
Defines the Piece class used by the chess engine.
Each piece knows its color ('W' or 'B'), its type ('K','Q','R','B','N','P')
and whether it has moved (needed for castling rights and pawn double-pushes).
'''
class Piece:
    """A single chess piece."""
    # Mapping (color, type) -> unicode glyph
    SYMBOLS = {
        ('W', 'K'): 'K', ('W', 'Q'): 'Q', ('W', 'R'): 'R',
        ('W', 'B'): 'B', ('W', 'N'): 'N', ('W', 'P'): 'P',
        ('B', 'K'): 'k', ('B', 'Q'): 'q', ('B', 'R'): 'r',
        ('B', 'B'): 'b', ('B', 'N'): 'n', ('B', 'P'): 'p',
    }
    def __init__(self, color, piece_type):
        self.color = color  # 'W' or 'B'
        self.type = piece_type  # 'K','Q','R','B','N','P'
        self.has_moved = False
    @property
    def symbol(self):
        """Single-character glyph: uppercase for White, lowercase for Black."""
        return self.SYMBOLS[(self.color, self.type)]
    def __repr__(self):
        return "Piece({}, {})".format(self.color, self.type)