'''
game.py
Game controller: turn alternation, mandatory-capture enforcement,
multi-jump continuation, kinging feedback, and win/draw detection.
'''
from board import Board
from pieces import PieceColor
from rules import all_moves, moves_for_piece, jump_targets
class Game:
    def __init__(self):
        self.board = Board()
        self.current = PieceColor.RED
        self.captured = {PieceColor.RED: [], PieceColor.BLACK: []}  # pieces captured BY each color
        self.chain_pos = None  # (row, col) if a multi-jump is in progress
        self.quiet_moves = 0   # plies without capture (draw detection)
    def legal_moves(self):
        if self.chain_pos:
            return moves_for_piece(self.board, *self.chain_pos, jumps_only=True)
        return all_moves(self.board, self.current)
    def apply(self, move):
        """Apply one validated move segment; manages chains and turns."""
        piece = self.board.get_piece(*move.start)
        captured_piece = self.board.get_piece(*move.captured) if move.is_jump else None
        crowned = self.board.apply_move(move)
        if move.is_jump:
            self.captured[self.current].append(captured_piece)
            self.quiet_moves = 0
        else:
            self.quiet_moves += 1
        # Continuation: same piece must keep jumping (unless just crowned).
        if move.is_jump and not crowned:
            further = jump_targets(self.board, *move.end, piece)
            if further:
                self.chain_pos = move.end
                return
        self.chain_pos = None
        self.current = self.current.opponent
    def status(self):
        """Return 'ongoing', 'red_wins', 'black_wins', or 'draw'."""
        red = self.board.count_pieces(PieceColor.RED)
        black = self.board.count_pieces(PieceColor.BLACK)
        if red == 0:
            return 'black_wins'
        if black == 0:
            return 'red_wins'
        if not all_moves(self.board, self.current):
            # A player who cannot move loses.
            return 'black_wins' if self.current is PieceColor.RED else 'red_wins'
        if self.quiet_moves >= 80:  # 40 moves each side without capture or man advancement → draw
            return 'draw'
        return 'ongoing'