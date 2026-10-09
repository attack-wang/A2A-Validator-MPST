'''
game.py
Defines the Game class: the rules engine that owns the board, side to
move, castling rights, en-passant square, clocks, move history and
repetition counts. It generates legal moves, applies them, detects
check / checkmate / stalemate / draws and supports undo.
'''
from board import Board
from move import Move
from piece import Pawn, King, Rook, make_piece
class Game:
    """Full chess rules engine for two-player terminal play."""
    def __init__(self):
        self.board = Board()
        self.turn = 'w'
        # Castling rights: king-side / queen-side for each color.
        self.castling = {'wK': True, 'wQ': True, 'bK': True, 'bQ': True}
        self.ep_square = None      # (row, col) en-passant target square
        self.halfmove = 0          # plies since last pawn move / capture
        self.fullmove = 1
        self.history = []          # stack of undo records
        self.position_counts = {}  # FEN-like key -> occurrences (repetition)
        self._record_position()
    # ------------------------------------------------------------------
    # Position keys & repetition
    # ------------------------------------------------------------------
    def _position_key(self):
        """A string describing the position for repetition purposes:
        piece placement, side to move, castling rights, ep square."""
        rows = []
        for r in range(8):
            row = ''
            for c in range(8):
                p = self.board.get(r, c)
                row += p.char() if p else '.'
            rows.append(row)
        rights = ''.join(k for k, v in sorted(self.castling.items()) if v) or '-'
        ep = str(self.ep_square) if self.ep_square else '-'
        return '|'.join(rows) + f'|{self.turn}|{rights}|{ep}'
    def _record_position(self):
        key = self._position_key()
        self.position_counts[key] = self.position_counts.get(key, 0) + 1
    # ------------------------------------------------------------------
    # Check detection
    # ------------------------------------------------------------------
    def is_in_check(self, color):
        """True if `color`'s king is attacked by the opponent."""
        king = self.board.find_king(color)
        if king is None:
            return False
        return self.board.is_attacked(king[0], king[1],
                                      'b' if color == 'w' else 'w')
    def _leaves_king_safe(self, move, color):
        """Simulate `move` and return True if `color`'s king is not left
        (or becomes) in check."""
        saved = self._snapshot_state()
        self._apply_move(move)
        safe = not self.is_in_check(color)
        self._restore_state(saved)
        return safe
    # ------------------------------------------------------------------
    # Move generation
    # ------------------------------------------------------------------
    def _pseudo_moves(self, color):
        """All pseudo-legal moves for `color` (including castling)."""
        moves = []
        for r in range(8):
            for c in range(8):
                p = self.board.get(r, c)
                if p is None or p.color != color:
                    continue
                for (er, ec) in p.pseudo_moves(self.board, r, c, self.ep_square):
                    target = self.board.get(er, ec)
                    is_ep = (isinstance(p, Pawn) and self.ep_square == (er, ec)
                             and target is None)
                    move = Move((r, c), (er, ec), p,
                                captured=target,
                                captured_square=(er, ec) if target is not None
                                else ((er, ec) if is_ep else None),
                                is_en_passant=is_ep)
                    # Promotion: reaching the last rank with a pawn.
                    if isinstance(p, Pawn) and (er == 0 or er == 7):
                        for promo in ('Q', 'R', 'B', 'N'):
                            pm = Move((r, c), (er, ec), p,
                                      captured=target,
                                      captured_square=(er, ec) if target is not None else None,
                                      promotion=promo, is_en_passant=False)
                            moves.append(pm)
                    else:
                        moves.append(move)
        moves.extend(self.castling_moves(color))
        return moves
    def castling_moves(self, color):
        """Generate legal castling moves for `color` (as Move objects with
        is_castle set). Verifies rights, empty squares, rook presence and
        that the king does not pass through or land on an attacked square."""
        moves = []
        row = 7 if color == 'w' else 0
        enemy = 'b' if color == 'w' else 'w'
        king = self.board.get(row, 4)
        if not isinstance(king, King) or king.color != color:
            return moves
        if self.is_in_check(color):
            return moves
        # King-side: king e->g, rook h->f; squares f and g empty.
        if self.castling.get(color + 'K'):
            rook = self.board.get(row, 7)
            if isinstance(rook, Rook) and rook.color == color \
                    and self.board.get(row, 5) is None \
                    and self.board.get(row, 6) is None \
                    and not self.board.is_attacked(row, 5, enemy) \
                    and not self.board.is_attacked(row, 6, enemy):
                moves.append(Move((row, 4), (row, 6), king,
                                  is_castle='K'))
        # Queen-side: king e->c, rook a->d; squares b, c, d empty.
        if self.castling.get(color + 'Q'):
            rook = self.board.get(row, 0)
            if isinstance(rook, Rook) and rook.color == color \
                    and self.board.get(row, 1) is None \
                    and self.board.get(row, 2) is None \
                    and self.board.get(row, 3) is None \
                    and not self.board.is_attacked(row, 3, enemy) \
                    and not self.board.is_attacked(row, 2, enemy):
                moves.append(Move((row, 4), (row, 2), king,
                                  is_castle='Q'))
        return moves
    def legal_moves(self, color=None):
        """All fully legal moves for `color` (defaults to side to move):
        pseudo-legal moves filtered so the mover's king is never left in
        check. Castling legality (transit squares) is already enforced in
        castling_moves, but the final king-safety check is re-applied
        harmlessly."""
        if color is None:
            color = self.turn
        return [m for m in self._pseudo_moves(color)
                if self._leaves_king_safe(m, color)]