'''
game_logic.py
This module defines the TicTacToeGame class, which manages the flow of a
tic-tac-toe match on top of the Board model. It keeps track of whose turn
it is, applies player moves, detects wins and draws, and supports
starting a new round. Like Board, it is completely independent of any
user-interface technology.
'''
from board import Board
class TicTacToeGame:
    """Turn-based controller for a two-player tic-tac-toe match."""
    PLAYER_X = "X"
    PLAYER_O = "O"
    def __init__(self):
        """Create a new game with an empty board; player X moves first."""
        self._board = Board()
        self._current_player = self.PLAYER_X
        self._game_over = False
        self._winner = None
        self._winning_line = None
    # -- properties -------------------------------------------------
    @property
    def board(self):
        """The Board instance used by this game."""
        return self._board
    @property
    def current_player(self):
        """Mark ('X' or 'O') of the player who should move next."""
        return self._current_player
    @property
    def game_over(self):
        """True when the match has been won or ended in a draw."""
        return self._game_over
    @property
    def winner(self):
        """Winning mark, or None when the game is still running/a draw."""
        return self._winner
    @property
    def winning_line(self):
        """Tuple of cells that form the winning line, or None."""
        return self._winning_line
    # -- game flow ---------------------------------------------------
    def make_move(self, row, col):
        """
        Attempt to place the current player's mark at (row, col).
        Returns True if the move was legal and applied. A legal move on a
        running game also triggers win/draw detection and, when the game
        continues, hands the turn over to the other player.
        """
        if self._game_over:
            return False
        if not self._board.place_mark(row, col, self._current_player):
            return False
        winner, line = self._board.get_winning_line()
        if winner is not None:
            self._winner = winner
            self._winning_line = line
            self._game_over = True
        elif self._board.is_full():
            self._game_over = True  # draw: winner stays None
        else:
            self._switch_player()
        return True
    def _switch_player(self):
        """Alternate the turn between X and O."""
        self._current_player = (self.PLAYER_O
                                if self._current_player == self.PLAYER_X
                                else self.PLAYER_X)
    def is_draw(self):
        """True when the board is full and nobody has won."""
        return self._game_over and self._winner is None
    def reset(self):
        """Start a fresh round; X always begins."""
        self._board.reset()
        self._current_player = self.PLAYER_X
        self._game_over = False
        self._winner = None
        self._winning_line = None