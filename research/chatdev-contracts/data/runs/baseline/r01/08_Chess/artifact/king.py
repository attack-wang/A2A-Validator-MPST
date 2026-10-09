# pieces.py
'''
Piece definitions for the chess game.
'''
WHITE = 'w'
BLACK = 'b'
class Piece:
    """Base class for all chess pieces."""
    def __init__(self, color, piece_type):
        self.color = color
        self.piece_type = piece_type
        self.has_moved = False
    @property
    def symbol(self):
        """Uppercase letter for the piece type."""
        return self.piece_type
    def display(self):
        """Character used to display the piece on the board."""
        s = self.piece_type
        return s if self.color == WHITE else s.lower()
    def value(self):
        return {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}[self.piece_type]
    def __repr__(self):
        return f"{self.color}{self.piece_type}"
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'P')
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'N')
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'B')
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'R')
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'Q')
class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'K')