'''
game.py
This module defines the Game class, which manages the overall flow of a
Reversi match on top of the Board. It handles:
- Turn alternation between the two players (BLACK and WHITE)
- Applying legal moves and flipping discs via the Board
- Automatic "pass" handling when a player has no legal moves
- Detecting the end of the game (board full or neither player can move)
- Determining the winner and exposing the current score
'''
from board import Board, BLACK, WHITE, EMPTY
class Game:
    """Controller for a full Reversi game session."""
    def __init__(self):
        self.board = Board()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None  # BLACK, WHITE, or None (draw)
        self.last_move = None  # (row, col) of the most recent placement
        self.last_flipped = []  # discs flipped by the most recent move
        self.passed_last_turn = False  # True if the previous turn was a pass
    def get_valid_moves(self):
        """Return all legal moves for the current player."""
        return self.board.get_valid_moves(self.current_player)
    def make_move(self, row, col):
        """
        Attempt to play the current player's disc on (row, col).
        Returns True if the move was legal and applied, False otherwise.
        After a successful move, turn handling and game-over checks run.
        """
        if self.game_over:
            return False
        flipped = self.board.place_disc(row, col, self.current_player)
        if flipped is None:
            return False
        self.last_move = (row, col)
        self.last_flipped = flipped
        self.passed_last_turn = False
        self._advance_turn()
        return True
    def pass_turn(self):
        """
        Forfeit the current player's turn (only legal when they have no
        valid moves). Returns True if the pass was applied.
        """
        if self.game_over:
            return False
        if self.board.has_valid_move(self.current_player):
            return False
        self.passed_last_turn = True
        self.last_move = None
        self.last_flipped = []
        self._advance_turn()
        return True
    def _advance_turn(self):
        """
        Switch to the other player, applying automatic pass rules, and
        update the game-over state.
        """
        opponent = -self.current_player
        if self.board.has_valid_move(opponent):
            self.current_player = opponent
        elif self.board.has_valid_move(self.current_player):
            # Opponent must pass; current player keeps playing.
            self.passed_last_turn = True
        else:
            # Neither side can move: the game is over.
            self._end_game()
            return
        # End the game when the board is completely full.
        if self.board.is_full():
            self._end_game()
    def _end_game(self):
        """Finalize the game: compute the winner from the final score."""
        self.game_over = True
        score = self.board.get_score()
        if score['black'] > score['white']:
            self.winner = BLACK
        elif score['white'] > score['black']:
            self.winner = WHITE
        else:
            self.winner = None  # Draw
    def is_game_over(self):
        """Return True if the game has finished."""
        return self.game_over
    def get_score(self):
        """Return the current score dictionary from the board."""
        return self.board.get_score()
    def get_winner(self):
        """Return the winner (BLACK/WHITE) or None for a draw/ongoing game."""
        return self.winner