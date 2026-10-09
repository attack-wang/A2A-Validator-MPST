'''
game.py
This module implements the Game class, which manages the overall Reversi
game flow: turn alternation, move application, pass handling when a player
has no valid moves, score tracking, and game-over detection. The turn-
advancement logic is fully implemented here, and a `passed_player` flag is
exposed so the UI can inform users when a player is forced to pass.
'''
from constants import BLACK, WHITE
from board import Board
class Game:
    """Manages the state and flow of a Reversi match."""
    def __init__(self):
        """Create a new game with a fresh board; Black always moves first."""
        self.board = Board()
        self.current_player = BLACK
        self.last_move = None      # (row, col) of the most recent placement
        self.last_flipped = []     # discs flipped by the most recent move
        self.passed_player = None  # player who had to pass on the last turn
        self.game_over = False
        self.winner = None
    def reset(self):
        """Reset the game to its initial state."""
        self.board.reset()
        self.current_player = BLACK
        self.last_move = None
        self.last_flipped = []
        self.passed_player = None
        self.game_over = False
        self.winner = None
    def get_current_player(self):
        """Return the player code whose turn it is."""
        return self.current_player
    def get_passed_player(self):
        """Return the player who had to pass on the last turn, or None."""
        return self.passed_player
    def get_valid_moves(self):
        """Return all valid moves for the current player."""
        return self.board.get_valid_moves(self.current_player)
    def has_valid_move(self, player):
        """Return True if the given player has at least one valid move."""
        return len(self.board.get_valid_moves(player)) > 0
    def try_move(self, row, col):
        """
        Attempt to place the current player's disc at (row, col).
        Returns True if the move was applied (turn passes accordingly),
        False if the move is invalid or the game is already over.
        """
        if self.game_over:
            return False
        if not self.board.is_valid_move(row, col, self.current_player):
            return False
        flipped = self.board.place_disc(row, col, self.current_player)
        self.last_move = (row, col)
        self.last_flipped = flipped
        self._advance_turn()
        return True
    def _advance_turn(self):
        """
        Hand the turn to the opponent, skipping a player who has no valid
        moves, and detect whether the game has ended.
        """
        opponent = WHITE if self.current_player == BLACK else BLACK
        # Game ends when the board is completely full.
        if self.board.is_full():
            self.game_over = True
            self._determine_winner()
            self.passed_player = None
            return
        if self.has_valid_move(opponent):
            self.current_player = opponent
            self.passed_player = None
        elif self.has_valid_move(self.current_player):
            # Opponent has no valid move and must pass; current player continues.
            self.passed_player = opponent
        else:
            # Neither player can move: the game ends.
            self.game_over = True
            self._determine_winner()
            self.passed_player = None
    def _determine_winner(self):
        """Set the winner based on the current disc counts."""
        black, white = self.board.count_discs()
        if black > white:
            self.winner = BLACK
        elif white > black:
            self.winner = WHITE
        else:
            self.winner = None  # Draw
    def is_game_over(self):
        """Return True when the board is full or no valid moves remain."""
        return self.game_over
    def get_score(self):
        """Return a dict with the current disc counts for both players."""
        black, white = self.board.count_discs()
        return {BLACK: black, WHITE: white}
    def get_winner(self):
        """Return the winning player's code, or None for a draw/ongoing game."""
        return self.winner