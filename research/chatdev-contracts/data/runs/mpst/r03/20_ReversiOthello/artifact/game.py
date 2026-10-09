'''
game.py
This module implements the game logic layer for Reversi (Othello). It manages
the two players, turn order, automatic pass handling when a player has no
legal move, and detection of the end of the game.
'''
from board import Board
class Player:
    """Represents one of the two Reversi players."""
    def __init__(self, name, disc):
        self.name = name
        self.disc = disc
    @property
    def color_name(self):
        """Human readable colour of the player's discs."""
        return "Black" if self.disc == Board.BLACK else "White"
class Game:
    """Controls the flow of a Reversi match between two players."""
    def __init__(self):
        self.board = Board()
        self.players = [Player("Player 1", Board.BLACK), Player("Player 2", Board.WHITE)]
        self.current_index = 0
        self.game_over = False
        self.winner = None
        self.status_message = "Black moves first. Click a highlighted square."
    @property
    def current_player(self):
        return self.players[self.current_index]
    def other_player(self):
        return self.players[1 - self.current_index]
    def valid_moves(self):
        return self.board.get_valid_moves(self.current_player.disc)
    def make_move(self, row, col):
        """
        Attempt to play the current player's disc on (row, col).
        Returns the list of flipped positions, or None when the move is
        illegal. Updates turn order, pass messages and game-over state.
        """
        if self.game_over:
            return None
        disc = self.current_player.disc
        if not self.board.is_valid_move(row, col, disc):
            return None
        flipped = self.board.apply_move(row, col, disc)
        self._advance_turn()
        return flipped
    def _advance_turn(self):
        """Hand the turn over, skipping players without legal moves."""
        next_index = 1 - self.current_index
        next_player = self.players[next_index]
        if self.board.has_valid_move(next_player.disc):
            self.current_index = next_index
            self.status_message = f"{next_player.color_name}'s turn."
        elif self.board.has_valid_move(self.current_player.disc):
            # Next player must pass; current player moves again.
            self.status_message = (
                f"{next_player.color_name} has no valid move and must pass. "
                f"{self.current_player.color_name} moves again."
            )
        else:
            # Neither side can move: the game is finished.
            self._finish_game()
        if self.board.is_full() and not self.game_over:
            self._finish_game()
    def _finish_game(self):
        """Mark the game as over and determine the winner."""
        self.game_over = True
        black = self.board.count_discs(Board.BLACK)
        white = self.board.count_discs(Board.WHITE)
        if black > white:
            self.winner = self.players[0]
        elif white > black:
            self.winner = self.players[1]
        else:
            self.winner = None
        self.status_message = "Game over."
    def scores(self):
        """Return a dict mapping colour names to disc counts."""
        return {
            "Black": self.board.count_discs(Board.BLACK),
            "White": self.board.count_discs(Board.WHITE),
        }
    def restart(self):
        """Reset everything for a fresh match."""
        self.__init__()