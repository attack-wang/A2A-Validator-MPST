'''
game.py
Rules engine for standard American/English checkers (draughts).
Responsibilities:
  * generate every legal move for the side to play (captures are
    mandatory and multi-jumps must be played out completely)
  * validate and apply moves on the board, removing captured pieces
  * crown men that reach the far rank (a man that is crowned in the
    middle of a multi-jump stops there, per the standard rules)
  * alternate turns and detect when the game is over
'''
from board import Board, BOARD_SIZE
from piece import Piece, PieceColor
from move import Move
class IllegalMoveError(ValueError):
    """Raised when a move is not among the legal moves for the turn."""
class Game:
    """Rules engine and state machine for one checkers game."""
    def __init__(self, board=None):
        self._board = board if board is not None else Board()
        self._turn = PieceColor.RED  # Red moves first in this implementation
    @property
    def board(self):
        return self._board
    @property
    def turn(self):
        return self._turn
    # ------------------------------------------------------------------
    # Move generation
    # ------------------------------------------------------------------
    def legal_moves(self, color=None):
        """All legal moves for `color` (the side to play by default).
        Captures are mandatory: if any capture exists, only capture
        sequences are returned.
        """
        color = color if color is not None else self._turn
        captures = []
        steps = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self._board.get_piece(row, col)
                if piece is None or piece.color is not color:
                    continue
                captures.extend(self._captures_from((row, col), piece))
                steps.extend(self._steps_from((row, col), piece))
        return captures if captures else steps
    def _steps_from(self, start, piece):
        """Simple non-capturing diagonal steps for one piece."""
        results = []
        row, col = start
        for dr, dc in piece.directions():
            land = (row + dr, col + dc)
            if self._board.is_empty(*land):
                results.append(Move([start, land]))
        return results
    def _captures_from(self, start, piece):
        """Every complete capture sequence beginning at `start`."""
        results = []
        king_row = self._board.king_row(piece.color)
        def explore(pos, path, captured, is_king_now):
            row, col = pos
            extended = False
            for dr, dc in (piece.directions() if is_king_now else piece.directions()):