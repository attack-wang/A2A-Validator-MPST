'''
move.py
Defines the Move class: a single chess move described by its start square,
end square, moving piece and optional flags (capture, en passant, castling,
double pawn push, promotion).
Squares are (row, col) tuples with row 0 = rank 8 and col 0 = file 'a'.
'''
FILE_CHARS = 'abcdefgh'
def square_name(square):
    """Convert an internal (row, col) square to algebraic name, e.g. (7,4) -> 'e1'."""
    row, col = square
    return FILE_CHARS[col] + str(8 - row)
def parse_square(name):
    """Convert an algebraic square name, e.g. 'e1', to internal (row, col)."""
    name = name.strip().lower()
    if len(name) != 2 or name[0] not in FILE_CHARS or name[1] not in '12345678':
        raise ValueError("Bad square: %r" % (name,))
    col = FILE_CHARS.index(name[0])
    row = 8 - int(name[1])
    return (row, col)
class Move:
    """One chess move with all information needed to apply and undo it."""
    def __init__(self, start, end, piece, captured=None, promotion=None,
                 is_en_passant=False, is_castle_king=False,
                 is_castle_queen=False, is_double_push=False):
        self.start = start              # (row, col)
        self.end = end                  # (row, col)
        self.piece = piece              # Piece being moved
        self.captured = captured        # Piece captured (None if none); for e.p. this is the captured pawn
        self.promotion = promotion      # 'Q', 'R', 'B', 'N' or None
        self.is_en_passant = is_en_passant
        self.is_castle_king = is_castle_king
        self.is_castle_queen = is_castle_queen
        self.is_double_push = is_double_push
    # --- helpers -----------------------------------------------------------
    @property
    def is_capture(self):
        return self.captured is not None
    @property
    def is_castle(self):
        return self.is_castle_king or self.is_castle_queen
    def to_algebraic(self, legal_moves=None):
        """Return a SAN string for this move.
        `legal_moves` (all legal moves in the position) is optional; when
        given it is used to compute correct disambiguation (e.g. 'Nbd2').
        """
        if self.is_castle_king:
            return 'O-O'
        if self.is_castle_queen:
            return 'O-O-O'
        piece_type = self.piece.piece_type
        letter = '' if piece_type == 'P' else piece_type
        # Disambiguation among identical piece types reaching the same square.
        disambig = ''
        if legal_moves and piece_type != 'P':
            others = [m for m in legal_moves
                      if m.piece.piece_type == piece_type
                      and m.end == self.end
                      and m.start != self.start
                      and not m.is_castle]
            if others:
                same_file = any(m.start[1] == self.start[1] for m in others)
                same_rank = any(m.start[0] == self.start[0] for m in others)
                if not same_file:
                    disambig = FILE_CHARS[self.start[1]]
                elif not same_rank:
                    disambig = str(8 - self.start[0])
                else:
                    disambig = square_name(self.start)
        capture = ''
        if piece_type == 'P':
            if self.is_capture or self.is_en_passant:
                capture = FILE_CHARS[self.start[1]] + 'x'
        elif self.is_capture:
            capture = 'x'
        promo = '=' + self.promotion if self.promotion else ''
        return letter + disambig + capture + square_name(self.end) + promo
    def __eq__(self, other):
        return (isinstance(other, Move) and self.start == other.start and
                self.end == other.end and self.promotion == other.promotion)
    def __hash__(self):
        return hash((self.start, self.end, self.promotion))
    def __repr__(self):
        return "Move(%s->%s%s)" % (square_name(self.start), square_name(self.end),
                                   '=' + self.promotion if self.promotion else '')