'''
game_controller.py
This module orchestrates the flow of a Gomoku match. The GameController binds
the pure game logic (Board) to the turn system, tracks whose turn it is,
applies moves, evaluates win/draw conditions after every move, records the
last played move and exposes the current game state to the presentation layer.
'''
from constants import GameState, PLAYER_BLACK
from board import Board
from player import Player
class GameController:
    """Manages turns, move application and win/draw evaluation."""
    def __init__(self, board=None):
        self._board = board if board is not None else Board()
        self._black = Player(PLAYER_BLACK)
        self._white = self._black.opponent
        self._current_player = self._black
        self._state = GameState.ONGOING
        self._winning_line = None
        self._last_move = None
    # --- Read-only accessors -------------------------------------------
    @property
    def board(self):
        return self._board
    @property
    def current_player(self):
        return self._current_player
    @property
    def state(self):
        return self._state
    @property
    def winning_line(self):
        return self._winning_line
    @property
    def last_move(self):
        """Return the (row, col) of the most recently played stone, or None."""
        return self._last_move
    def is_game_over(self):
        """Return True when the match has been won or ended in a draw."""
        return self._state is not GameState.ONGOING
    def reset(self):
        """Start a fresh game: empty board, Black moves first."""
        self._board.reset()
        self._current_player = self._black
        self._state = GameState.ONGOING
        self._winning_line = None
        self._last_move = None
    def try_make_move(self, row, col):
        """
        Attempt to play the current player's stone at (row, col).
        Returns True when the move was applied. After a legal move the method
        evaluates the board, updates the game state and, if the game is still
        ongoing, hands the turn over to the opponent.
        """
        if self.is_game_over():
            return False
        if not self._board.place_stone(row, col, self._current_player.player_id):
            return False
        self._last_move = (row, col)
        winning_line = self._board.check_win(row, col)
        if winning_line is not None:
            self._winning_line = winning_line
            self._state = (GameState.BLACK_WIN
                           if self._current_player.player_id == PLAYER_BLACK
                           else GameState.WHITE_WIN)
            return True
        if self._board.is_full():
            self._state = GameState.DRAW
            return True
        self._current_player = self._current_player.opponent
        return True