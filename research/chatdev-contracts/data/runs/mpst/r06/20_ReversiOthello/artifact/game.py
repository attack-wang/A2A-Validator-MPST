"""
game.py
Turn management for the Reversi (Othello) game.
The `Game` class wraps a `Board` and two `Player` objects, tracks whose
turn it is, applies moves, handles automatic passes when a player has
no legal move, detects the end of the game and determines the winner.
"""
from board import Board, BLACK, WHITE, COLOR_NAMES
from player import Player
class Game:
    """Coordinates the flow of a full Reversi match."""
    def __init__(self, black_name=None, white_name=None):
        self.board = Board()
        self.players = {
            BLACK: Player(BLACK, black_name),
            WHITE: Player(WHITE, white_name),
        }
        self.current_color = BLACK  # Black always moves first.
        self.game_over = False
        self.winner_color = None
        self.last_move = None       # (row, col) of the most recent disc
        self.last_flipped = []      # discs flipped by the most recent move
        self.passed_colors = []     # colours forced to pass since last move
    # -- queries -------------------------------------------------------
    @property
    def current_player(self):
        return self.players[self.current_color]
    def get_valid_moves(self):
        return self.board.get_valid_moves(self.current_color)
    def is_valid_move(self, row, col):
        return self.board.is_valid_move(self.current_color, row, col)
    def get_score(self):
        return self.board.get_score()
    def get_winner(self):
        """Return the winning Player, or None for a draw / ongoing game."""
        if not self.game_over:
            return None
        score = self.board.get_score()
        if score[BLACK] > score[WHITE]:
            return self.players[BLACK]
        if score[WHITE] > score[BLACK]:
            return self.players[WHITE]
        return None  # draw
    # -- actions ---------------------------------------------------------
    def apply_move(self, row, col):
        """
        Play the current player's disc on (row, col).
        Returns True when the move was legal and applied, False otherwise.
        Updates turn ownership, records forced passes and detects the end
        of the game.
        """
        if self.game_over:
            return False
        if not self.board.is_valid_move(self.current_color, row, col):
            return False
        self.last_flipped = self.board.get_flippable_discs(self.current_color, row, col)
        self.board.place_disc(self.current_color, row, col)
        self.last_move = (row, col)
        self.passed_colors = []
        self._advance_turn()
        return True
    def _advance_turn(self):
        """Hand the turn over, forcing passes / ending the game as needed."""
        opponent = 3 - self.current_color
        if self.board.is_game_over():
            self.game_over = True
            self.winner_color = self._winner_color()
            return
        if self.board.has_valid_move(opponent):
            self.current_color = opponent
        else:
            # Opponent cannot move: they pass and the current player goes
            # again. (The board cannot be over here because is_game_over
            # was already checked above.)
            self.passed_colors.append(opponent)
    def _winner_color(self):
        score = self.board.get_score()
        if score[BLACK] > score[WHITE]:
            return BLACK
        if score[WHITE] > score[BLACK]:
            return WHITE
        return None