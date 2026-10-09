'''
board.py
Contains the Board class: 8x8 grid representation, piece placement,
pseudo-legal and legal move generation, attack detection, applying moves,
castling rights / en passant tracking, and terminal rendering.
'''
from pieces import Piece, WHITE, BLACK, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING
from move import Move
# Direction helpers
KNIGHT_OFFSETS = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1))
KING_OFFSETS = ((-1, -1), (-1, 0), (-1, 1),
                (0, -1),           (0, 1),
                (1, -1), (1, 0), (1, 1))
ROOK_DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))
BISHOP_DIRS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
FILES = 'abcdefgh'
def square_name(row, col):
    """Convert (row, col) with row 0 = rank 8 into algebraic name, e.g. (7,4) -> 'e1'."""
    return FILES[col] + str(8 - row)
class Board:
    def __init__(self):
        back = [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK]
        self.grid = [[None] * 8 for _ in range(8)]
        for c in range(8):
            self.grid[0][c] = Piece(BLACK, back[c])
            self.grid[1][c] = Piece(BLACK, PAWN)
            self.grid[6][c] = Piece(WHITE, PAWN)
            self.grid[7][c] = Piece(WHITE, back[c])
        self.turn = WHITE
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = None  # (row, col) or None
        self.halfmove_clock = 0
        self.fullmove_number = 1