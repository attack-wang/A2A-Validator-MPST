'''
game.py
Core checkers rules: turn management, legal move generation (mandatory captures,
multi-jumps), kinging, win/draw detection, and incremental move execution with
rollback on invalid input.
'''
from piece import Piece, RED, BLACK
from board import Board
from move_parser import MoveError, square_name
MAX_QUIET_HALFMOVES = 80  # 40 moves per side without capture or crowning → draw
class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = RED
        self.game_over = False
        self.winner = None
        self.is_draw = False
        self.quiet_halfmoves = 0
        self.last_move_desc = None
    # ---------- queries ----------
    def directions_for(self, piece):
        if piece.is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece.color == RED:
            return [(1, -1), (1, 1)]   # red moves toward rank 8 (row 7)
        return [(-1, -1), (-1, 1)]     # black moves toward rank 1 (row 0)
    def capture_targets(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece is None:
            return []
        targets = []
        for dr, dc in self.directions_for(piece):
            mr, mc = row + dr, col + dc
            tr, tc = row + 2 * dr, col + 2 * dc
            if not Board.in_bounds(tr, tc):
                continue
            mid = self.board.get_piece(mr, mc)
            if mid is None or mid.color == piece.color:
                continue
            if self.board.get_piece(tr, tc) is None:
                targets.append((tr, tc))
        return targets
    def simple_targets(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece is None:
            return []
        targets = []
        for dr, dc in self.directions_for(piece):
            tr, tc = row + dr, col + dc
            if Board.in_bounds(tr, tc) and self.board.get_piece(tr, tc) is None:
                targets.append((tr, tc))
        return targets
    def has_any_capture(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece is not None and piece.color == color:
                    if self.capture_targets(row, col):
                        return True
        return False
    def piece_moves(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece is None or piece.color != self.current_player:
            return []
        caps = self.capture_targets(row, col)
        if caps:
            return caps  # captures are mandatory when available
        if self.has_any_capture(self.current_player):
            return []    # another piece must capture instead
        return self.simple_targets(row, col)
    def player_moves(self, color):
        moves = []
        must_capture = self.has_any_capture(color)
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece is None or piece.color != color:
                    continue
                if must_capture:
                    for t in self.capture_targets(row, col):
                        moves.append(((row, col), t))
                else:
                    for t in self.simple_targets(row, col):
                        moves.append(((row, col), t))
        return moves