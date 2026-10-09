import copy  # maybe not needed here if board handles snapshot
from board import Board
from move import Move
from piece import Piece
class Game:
    """Owns the board, the turn order, the rule engine and the CLI loop."""
    RED = 'r'
    BLACK = 'b'
    DRAW_PLIES = 80   # plies without capture/man-advance before a draw
    def __init__(self, board=None):
        """Start a new game: fresh board (unless supplied), red to move."""
        self.board = board if board is not None else Board()
        self.current_color = Game.RED   # red always moves first
        self.quiet_plies = 0            # plies since last capture or man move
        self.game_over = False
        self.winner = None              # 'r'/'b' or 'draw' when finished