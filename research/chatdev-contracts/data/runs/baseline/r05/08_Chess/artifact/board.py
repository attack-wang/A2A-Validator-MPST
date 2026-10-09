'''
board.py
Board representation, pseudo-legal and legal move generation, move application,
castling/en-passant/promotion handling, and attack/check detection.
'''
from pieces import Piece, KNIGHT_OFFSETS, BISHOP_DIRS, ROOK_DIRS, KING_DIRS
from move import Move, parse_square, square_name
class Board:
    def __init__(self):
        self.reset()
    def reset(self):
        self.grid = [[None] * 8 for _ in range(8)]
        back = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for f in range(8):
            self.grid[0][f] = Piece('w', back[f])
            self.grid[1][f] = Piece('w', 'P')
            self.grid[6][f] = Piece('b', 'P')
            self.grid[7][f] = Piece('b', back[f])
        self.turn = 'w'
        self.castling = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant = None
        self.halfmove = 0
        self.fullmove = 1
        self.kings = {'w': (4, 0), 'b': (4, 7)}
    # --- basic helpers -------------------------------------------------
    def piece_at(self, sq):
        return self.grid[sq[1]][sq[0]]
    @staticmethod
    def opponent(color):
        return 'b' if color == 'w' else 'w'
    def in_bounds(self, sq):
        return 0 <= sq[0] < 8 and 0 <= sq[1] < 8
    def snapshot(self):
        return {
            'grid': [row[:] for row in self.grid],
            'turn': self.turn,
            'castling': dict(self.castling),
            'en_passant': self.en_passant,
            'halfmove': self.halfmove,
            'fullmove': self.fullmove,
            'kings': dict(self.kings),
        }
    def restore(self, snap):
        self.grid = [row[:] for row in snap['grid']]
        self.turn = snap['turn']
        self.castling = dict(snap['castling'])
        self.en_passant = snap['en_passant']
        self.halfmove = snap['halfmove']
        self.fullmove = snap['fullmove']
        self.kings = dict(snap['kings'])
    # --- attack detection ------------------------------------------------
    def is_attacked(self, sq, by_color):
        """Return True if square sq is attacked by any piece of by_color."""
        file_idx, rank_idx = sq
        # Pawn attacks
        pawn_dir = 1 if by_color == 'w' else -1  # white pawns move up (increasing rank)
        for df in (-1, 1):
            f, r = file_idx + df, rank_idx - pawn_dir
            if 0 <= f < 8 and 0 <= r < 8:
                p = self.grid[r][f]
                if p and p.color == by_color and p.kind == 'P':
                    return True
        # Knight attacks
        for df, dr in KNIGHT_OFFSETS:
            f, r = file_idx + df, rank_idx + dr
            if 0 <= f < 8 and 0 <= r < 8:
                p = self.grid[r][f]
                if p and p.color == by_color and p.kind == 'N':
                    return True
        # King attacks
        for df, dr in KING_DIRS:
            f, r = file_idx + df, rank_idx + dr
            if 0 <= f < 8 and 0 <= r < 8:
                p = self.grid[r][f]
                if p and p.color == by_color and p.kind == 'K':
                    return True
        # Sliding attacks: bishop/queen diagonals, rook/queen lines
        for dirs, kinds in ((BISHOP_DIRS, ('B', 'Q')), (ROOK_DIRS, ('R', 'Q'))):
            for df, dr in dirs:
                f, r = file_idx + df, rank_idx + dr
                while 0 <= f < 8 and 0 <= r < 8:
                    p = self.grid[r][f]
                    if p:
                        if p.color == by_color and p.kind in kinds:
                            return True
                        break
                    f += df
                    r += dr
        return False
    def in_check(self, color=None):
        color = color or self.turn
        return self.is_attacked(self.kings[color], self.opponent(color))