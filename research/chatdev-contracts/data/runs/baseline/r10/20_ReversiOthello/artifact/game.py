'''
game.py
This module contains the Game class, which manages the overall state of a
Reversi match: whose turn it is, applying moves, handling "pass" situations,
and detecting when the game is over.
'''
from board import Board, BLACK, WHITE
class Game:
    """Manages turn order, move application, and game-over detection."""
    def __init__(self):
        """Create a fresh board; black always moves first in Reversi."""
        self.board = Board()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None  # Set when the game ends
        self.message = ""   # Transient status message (e.g. "No valid move, pass")
    def reset(self):
        """Restore the game to its initial state so a new match can start."""
        self.board = Board()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None
        self.message = ""
    def handle_click(self, row, col):
        """
        Attempt to play the current player's disc at (row, col).
        Returns True if the move was legal and applied, otherwise False.
        """
        if self.game_over:
            return False
        if not self.board.is_valid_move(row, col, self.current_player):
            self.message = "Invalid move!"
            return False
        self.board.make_move(row, col, self.current_player)
        self.message = ""
        self._advance_turn()
        return True
    def _advance_turn(self):
        """
        Switch turns. If the next player has no valid move but the current
        one does, the next player passes. If neither player can move (which
        also covers a full board), the game is over.
        """
        next_player = self.board.get_opponent(self.current_player)
        if self.board.has_valid_move(next_player):
            self.current_player = next_player
        elif self.board.has_valid_move(self.current_player):
            # Next player must pass; current player moves again.
            self.message = "No valid move - pass!"
        else:
            # Board full or neither side can move: game over.
            self._end_game()
    def _end_game(self):
        """Mark the game as over and determine the winner (idempotent)."""
        if self.game_over:
            return  # Already ended; avoid processing the end state twice.
        self.game_over = True
        black, white = self.board.count_discs()
        if black > white:
            self.winner = BLACK
        elif white > black:
            self.winner = WHITE
        else:
            self.winner = None  # Draw
    def check_game_over(self):
        """
        Public safety check: end the game if the board is full or neither
        player has any valid move.
        """
        if self.board.is_full():
            self._end_game()
        elif (not self.board.has_valid_move(BLACK)
              and not self.board.has_valid_move(WHITE)):
            self._end_game()