'''
pieces.py
Defines the Piece class representing a chess piece with a type
('K', 'Q', 'R', 'B', 'N', 'P') and a color ('w' or 'b'), along with
Unicode glyph rendering and ASCII fallback symbols.
'''
class Piece:
    GLYPHS = {
        ('w', 'K'): '\u2654', ('w', 'Q'): '\u2655', ('w', 'R'): '\u2656',
        ('w', 'B'): '\u2657', ('w', 'N'): '\u2658', ('w', 'P'): '\u2659',
        ('b', 'K'): '\u265A', ('b', 'Q'): '\u265B', ('b', 'R'): '\u265C',
        ('b', 'B'): '\u265D', ('b', 'N'): '\u265E', ('b', 'P'): '\u265F',
    }
    ASCII = {
        ('w', 'K'): 'K', ('w', 'Q'): 'Q', ('w', 'R'): 'R',
        ('w', 'B'): 'B', ('w', 'N'): 'N', ('w', 'P'): 'P',
        ('b', 'K'): 'k', ('b', 'Q'): 'q', ('b', 'R'): 'r',
        ('b', 'B'): 'b', ('b', 'N'): 'n', ('b', 'P'): 'p',
    }
    def __init__(self, piece_type, color):
        if piece_type not in 'KQRBNP':
            raise ValueError(...)
        if color not in ('w', 'b'):
            raise ValueError(...)
        self.type = piece_type
        self.color = color
    def clone(self):
        return Piece(self.type, self.color)
    def symbol(self, use_unicode=True):
        if use_unicode:
            return self.GLYPHS[(self.color, self.type)]
        return self.ASCII[(self.color, self.type)]
    def __repr__(self):
        return f"Piece({self.ASCII[(self.color, self.type)]})"