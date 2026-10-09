'''
board.py
Implements the Board class: setup, attack detection, check/checkmate logic,
legal move generation, and application of moves including castling,
en passant and pawn promotion. Also re-exports Move for convenience.
'''
import re
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
from move import Move
class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.en_passant_target = None
        self._setup()
    def _setup(self):
        back = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for f in range(8):
            self.grid[0][f] = back[f]('b')
            self.grid[1][f] = Pawn('b')
            self.grid[6][f] = Pawn('w')
            self.grid[7][f] = back[f]('w')
    def in_bounds(self, f, r):
        return 0 <= f < 8 and 0 <= r < 8
    def get(self, f, r):
        return self.grid[r][f]
    def is_empty(self, f, r):
        return self.grid[r][f] is None
    @staticmethod
    def opponent(color):
        return 'b' if color == 'w' else 'w'
    def find_king(self, color):
        for r in range(8):
            for f in range(8):
                p = self.grid[r][f]
                if isinstance(p, King) and p.color == color:
                    return (f, r)
        return None
    def is_attacked(self, f, r, by_color):
        # pawn attackers
        dr = -1 if by_color == 'w' else 1
        for df in (-1, 1):
            pf, pr = f + df, r + dr
            if self.in_bounds(pf, pr):
                p = self.grid[pr][pf]
                if isinstance(p, Pawn) and p.color == by_color:
                    return True
        # knights
        for df, dr in Knight.OFFSETS:
            nf, nr = f + df, r + dr
            if self.in_bounds(nf, nr):
                p = self.grid[nr][nf]
                if isinstance(p, Knight) and p.color == by_color:
                    return True
        # enemy king adjacency
        for df, dr in King.DIRECTIONS:
            nf, nr = f + df, r + dr
            if self.in_bounds(nf, nr):
                p = self.grid[nr][nf]
                if isinstance(p, King) and p.color == by_color:
                    return True
        # rooks/queens on ranks/files
        for df, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nf, nr = f + df, r + dr
            while self.in_bounds(nf, nr):
                p = self.grid[nr][nf]
                if p is not None:
                    if p.color == by_color and isinstance(p, (Rook, Queen)):
                        return True
                    break
                nf += df
                nr += dr
        # bishops/queens on diagonals
        for df, dr in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            nf, nr = f + df, r + dr
            while self.in_bounds(nf, nr):
                p = self.grid[nr][nf]
                if p is not None:
                    if p.color == by_color and isinstance(p, (Bishop, Queen)):
                        return True
                    break
                nf += df
                nr += dr
        return False
    def in_check(self, color):
        ksq = self.find_king(color)
        if ksq is None:
            return False
        return self.is_attacked(ksq[0], ksq[1], self.opponent(color))
    def castling_targets(self, color):
        targets = []
        rank = 7 if color == 'w' else 0
        king = self.grid[rank][4]
        if not isinstance(king, King) or king.color != color or king.has_moved:
            return targets
        enemy = self.opponent(color)
        if self.is_attacked(4, rank, enemy):
            return targets
        rook = self.grid[rank][7]
        if (isinstance(rook, Rook) and rook.color == color and not rook.has_moved
                and self.is_empty(5, rank) and self.is_empty(6, rank)
                and not self.is_attacked(5, rank, enemy)
                and not self.is_attacked(6, rank, enemy)):
            targets.append((6, rank))
        rook = self.grid[rank][0]
        if (isinstance(rook, Rook) and rook.color == color and not rook.has_moved
                and self.is_empty(1, rank) and self.is_empty(2, rank)
                and self.is_empty(3, rank)
                and not self.is_attacked(3, rank, enemy)
                and not self.is_attacked(2, rank, enemy)):
            targets.append((2, rank))
        return targets
    def _pseudo_moves(self, color):
        moves = []
        promo_rank = 7 if color == 'w' else 0
        for r in range(8):
            for f in range(8):
                piece = self.grid[r][f]
                if piece is None or piece.color != color:
                    continue
                for (tf, tr) in piece.pseudo_legal_moves(self, f, r):
                    target = self.grid[tr][tf]
                    if isinstance(piece, Pawn) and tr == promo_rank:
                        for promo in ('Q', 'R', 'B', 'N'):
                            moves.append(Move((f, r), (tf, tr), piece, target, promotion=promo))
                    else:
                        ep = (isinstance(piece, Pawn)
                              and (tf, tr) == self.en_passant_target
                              and target is None)
                        moves.append(Move((f, r), (tf, tr), piece, target, is_en_passant=ep))
        return moves
    def _save_state(self):
        grid_copy = [row[:] for row in self.grid]
        moved = []
        for r in range(8):
            for f in range(8):
                p = self.grid[r][f]
                if p is not None:
                    moved.append((p, p.has_moved))
        return grid_copy, self.en_passant_target, moved
    def _restore_state(self, state):
        grid_copy, ept, moved = state
        self.grid = [row[:] for row in grid_copy]
        self.en_passant_target = ept
        for p, hm in moved:
            p.has_moved = hm
    def _apply(self, move):
        f, r = move.from_sq
        tf, tr = move.to_sq
        piece = self.grid[r][f]
        self.grid[tr][tf] = piece
        self.grid[r][f] = None
        piece.has_moved = True
        if move.is_en_passant:
            self.grid[r][tf] = None
        if move.is_castle:
            if tf == 6:
                self.grid[r][5] = self.grid[r][7]
                self.grid[r][7] = None
                self.grid[r][5].has_moved = True
            else:
                self.grid[r][3] = self.grid[r][0]
                self.grid[r][0] = None
                self.grid[r][3].has_moved = True
        if move.promotion:
            cls = {'Q': Queen, 'R': Rook, 'B': Bishop, 'N': Knight}[move.promotion]
            self.grid[tr][tf] = cls(piece.color)
        self.en_passant_target = None
        if isinstance(piece, Pawn) and abs(tr - r) == 2:
            self.en_passant_target = (f, (r + tr) // 2)
    def _is_legal(self, move, color):
        state = self._save_state()
        self._apply(move)
        ok = not self.in_check(color)
        self._restore_state(state)
        return ok
    def legal_moves(self, color):
        return [mv for mv in self._pseudo_moves(color) if self._is_legal(mv, color)]
    def make_move(self, move):
        self._apply(move)
    def render(self):
        lines = ['    a   b   c   d   e   f   g   h',
                 '  +---+---+---+---+---+---+---+---+']
        for r in range(7, -1, -1):
            row = f' {r + 1} '
            for f in range(8):
                p = self.grid[r][f]
                row += f'| {p.symbol if p else " "} '
            row += f'| {r + 1}'
            lines.append(row)
            lines.append('  +---+---+---+---+---+---+---+---+')
        return '\n'.join(lines)