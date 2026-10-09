'''
Base classes for chess pieces, including sliding pieces.
'''
class Piece:
    """Base class for all chess pieces."""
    def __init__(self, color):
        self.color = color  # 'w' or 'b'
        self.has_moved = False
    @property
    def letter(self):
        raise NotImplementedError
    @property
    def value(self):
        raise NotImplementedError
    def pseudo_moves(self, board, file, rank):
        raise NotImplementedError
    def __repr__(self):
        return f"{self.color}{self.letter}"
class SlidingPiece(Piece):
    """Piece that slides along DIRECTIONS until blocked."""
    DIRECTIONS = []
    def pseudo_moves(self, board, file, rank):
        return board.ray_moves(self, file, rank, self.DIRECTIONS)