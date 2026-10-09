'''
game.py
The Game class owns the board, the turn order and all rule enforcement:
legal-move generation with the forced-capture rule, multi-jump chaining,
kinging on the king row, and win/loss detection. It also parses moves
written in algebraic notation such as 'b6-a5'.
'''
import re
from piece import Piece, PieceColor
from board import Board
from constants import BOARD_SIZE, in_bounds, is_playable, to_notation
class Game:
    """Owns the board, the side to move, and all rule enforcement."""
    def __init__(self):
        """Set up the starting position; Black moves first (standard rules)."""
        self.board = Board()
        self.turn = PieceColor.BLACK
        self.mid_jump = None  # (row, col) of a piece that must keep jumping
    def get_legal_moves(self, color=None):
        """Return the list of legal moves as ((r1, c1), (r2, c2)) tuples.
        If any capture exists for the side to move, ONLY captures are legal
        (forced-capture rule). During a multi-jump, only the continuing
        jumps of the mid-jump piece are legal.
        """
        color = color if color is not None else self.turn
        jumps, steps = [], []
        if self.mid_jump is not None:
            sources = [self.mid_jump]
        else:
            sources = []
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    piece = self.board.get_piece(r, c)
                    if is_playable(r, c) and piece is not None and piece.color is color:
                        sources.append((r, c))
        for (r, c) in sources:
            piece = self.board.get_piece(r, c)
            for dr, dc in piece.capture_directions():
                mr, mc = r + dr, c + dc
                lr, lc = r + 2 * dr, c + 2 * dc
                middle = self.board.get_piece(mr, mc)
                landing = self.board.get_piece(lr, lc)
                if (in_bounds(lr, lc) and is_playable(lr, lc)
                        and middle is not None
                        and middle.color is color.opponent
                        and landing is None):
                    jumps.append(((r, c), (lr, lc)))
            if self.mid_jump is None:
                for dr, dc in piece.move_directions():
                    r2, c2 = r + dr, c + dc
                    if (in_bounds(r2, c2) and is_playable(r2, c2)
                            and self.board.get_piece(r2, c2) is None):
                        steps.append(((r, c), (r2, c2)))
        return jumps if jumps else steps
    def apply_move(self, src, dst):
        """Apply a validated legal move.
        Handles the captured-piece removal, kinging on the king row and
        multi-jump chaining. Returns True if the same player must move
        again (jump continuation), False if the turn switches.
        """
        piece = self.board.get_piece(*src)
        is_capture = abs(dst[0] - src[0]) == 2
        if is_capture:
            mid = ((src[0] + dst[0]) // 2, (src[1] + dst[1]) // 2)
            self.board.capture_piece(*mid)
        self.board.move_piece(src, dst)
        crowned = False
        if not piece.is_king and dst[0] == piece.color.king_row:
            piece.crown()
            crowned = True
        self.mid_jump = None
        if is_capture and not crowned:
            self.mid_jump = dst
            if self.get_legal_moves():
                return True
            self.mid_jump = None
        self.switch_turn()
        return False
    def switch_turn(self):
        """Hand the turn to the other player."""
        self.turn = self.turn.opponent
    def check_winner(self):
        """Return the winning color, or None while the game continues.
        A player loses when they have no pieces left or no legal move.
        """
        if self.board.count_pieces(PieceColor.RED) == 0:
            return PieceColor.BLACK
        if self.board.count_pieces(PieceColor.BLACK) == 0:
            return PieceColor.RED
        if not self.get_legal_moves():
            return self.turn.opponent
        return None
    def parse_move(self, text):
        """Parse 'b6-a5' (also 'b6xa5' or 'b6 a5') into ((r1, c1), (r2, c2)).
        Raises ValueError on malformed input.
        """
        match = re.fullmatch(
            r"\s*([a-hA-H])\s*([1-8])\s*[-xX ]\s*([a-hA-H])\s*([1-8])\s*", text)
        if not match:
            raise ValueError("Use notation like b6-a5 (file a-h, rank 1-8).")
        c1 = ord(match.group(1).lower()) - ord('a')
        r1 = BOARD_SIZE - int(match.group(2))
        c2 = ord(match.group(3).lower()) - ord('a')
        r2 = BOARD_SIZE - int(match.group(4))
        return (r1, c1), (r2, c2)