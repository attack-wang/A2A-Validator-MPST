'''
game.py
Core rules engine for English/American checkers (draughts):
* men move one square diagonally forward, kings in all four directions
* captures are mandatory; a jump chain must be continued as long as
  the same piece can keep jumping
* a man reaching the far rank is crowned king (and, per the standard
  rules, stops moving for that turn)
* a player loses when they have no pieces or no legal move
'''
from board import Board
from piece import PieceColor
from move import Move
# forward row deltas: red moves up the board (towards row 0)
FORWARD_DELTAS = {
    PieceColor.RED: (-1,),
    PieceColor.BLACK: (1,),
}
ALL_DELTAS = (-1, 1)
class Game:
    """State machine holding the board, the turn and the rules."""
    def __init__(self):
        self.board = Board()
        self._turn = PieceColor.BLACK   # standard rules: black moves first
    @property
    def turn(self):
        return self._turn
    def forward_rows(self, color):
        return FORWARD_DELTAS[color]
    def all_direction_rows(self):
        return ALL_DELTAS
    # -- move generation -------------------------------------------------
    def _directions_for(self, piece):
        """Row deltas the piece may travel: forward only for men, all four for kings."""
        if piece.is_king:
            return ALL_DELTAS
        return FORWARD_DELTAS[piece.color]
    def _step_targets(self, row, col, piece):
        """Empty squares reachable by a simple diagonal step."""
        targets = []
        for dr in self._directions_for(piece):
            for dc in (-1, 1):
                tr, tc = row + dr, col + dc
                if self.board.is_inside(tr, tc) and self.board.is_playable(tr, tc) \
                        and self.board.is_empty(tr, tc):
                    targets.append((tr, tc))
        return targets
    def _jump_targets(self, row, col, piece, captured):
        """Squares reachable by a single jump from (row, col).
        `captured` is the set of squares already stripped of pieces in the
        current chain (so a piece cannot be jumped twice).
        """
        targets = []
        enemy = piece.color.opposite
        for dr in self._directions_for(piece):
            for dc in (-1, 1):
                mr, mc = row + dr, col + dc       # midpoint (victim)
                tr, tc = row + 2 * dr, col + 2 * dc  # landing square
                if not self.board.is_inside(tr, tc) or not self.board.is_playable(tr, tc):
                    continue
                if (tr, tc) != (row, col) and not self.board.is_empty(tr, tc):
                    continue
                victim = self.board.get_piece(mr, mc)
                if victim is None or victim.color is not enemy:
                    continue
                if (mr, mc) in captured:
                    continue
                targets.append((tr, tc))
        return targets