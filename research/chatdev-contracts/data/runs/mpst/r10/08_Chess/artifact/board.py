'''
board.py
Chess board engine: setup, attack detection, legal move generation,
make/undo move, SAN parsing and SAN generation.
Coordinate convention:
    row 0 = rank 8 (black back rank), row 7 = rank 1 (white back rank)
    col 0 = file 'a', col 7 = file 'h'
'''
from pieces import Piece, create_piece
from move import Move
FILES = 'abcdefgh'
def square_name(pos):
    """Convert (row, col) to algebraic name, e.g. (7, 4) -> 'e1'."""
    row, col = pos
    return FILES[col] + str(8 - row)
def name_to_square(name):
    """Convert algebraic name like 'e1' to (row, col)."""
    name = name.lower()
    col = FILES.index(name[0])
    row = 8 - int(name[1])
    return (row, col)
def file_letter(col):
    return FILES[col]
def rank_number(row):
    return 8 - row
KNIGHT_OFFSETS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
KING_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)]
ROOK_DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
BISHOP_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.castling_rights = {'w': {'K': True, 'Q': True},
                                'b': {'K': True, 'Q': True}}
        self.en_passant_target = None   # (row, col) of the square that can be captured en passant
        self.setup()
    def setup(self):
        """Place pieces in the standard starting position."""
        back = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for c in range(8):
            self.grid[0][c] = create_piece(back[c], 'b')   # rank 8
            self.grid[1][c] = create_piece('P', 'b')       # rank 7
            self.grid[6][c] = create_piece('P', 'w')       # rank 2
            self.grid[7][c] = create_piece(back[c], 'w')   # rank 1
    # ---------- helpers ----------
    def piece_at(self, pos):
        return self.grid[pos[0]][pos[1]]
    def find_king(self, color):
        """Return (row, col) of the king of `color`."""
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p is not None and p.color == color and p.type == 'K':
                    return (r, c)
        return None
    def copy(self):
        """Deep-ish copy: new grid with copied pieces (has_moved matters)."""
        new = Board.__new__(Board)
        new.grid = [[None] * 8 for _ in range(8)]
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p is not None:
                    cp = create_piece(p.type, p.color)
                    cp.has_moved = p.has_moved
                    new.grid[r][c] = cp
        new.castling_rights = {c: dict(r) for c, r in self.castling_rights.items()}
        new.en_passant_target = self.en_passant_target
        return new