'''
game_controller.py
This module contains the GameController class, which manages the overall game
flow: whose turn it is, applying moves, detecting game-over states, and
tracking move history.
'''
from board import Board
from player import Player
class GameController:
    """Manages the state and flow of a tic-tac-toe game."""
    def __init__(self, player_x_name="Player 1", player_o_name="Player 2"):
        """Create a board, two players, and set the initial game state."""
        self.board = Board()
        self.players = {
            "X": Player("X", player_x_name),
            "O": Player("O", player_o_name),
        }
        self.current_symbol = "X"  # X always starts
        self.game_over = False
        self.winner_symbol = None
        self.move_history = []  # list of (symbol, row, col)
    def reset(self):
        """Reset the game to its initial state."""
        self.board.reset()
        self.current_symbol = "X"
        self.game_over = False
        self.winner_symbol = None
        self.move_history = []
    def get_current_player(self):
        """Return the Player object whose turn it is."""
        return self.players[self.current_symbol]
    def take_turn(self, row, col):
        """
        Attempt to place the current player's symbol at (row, col).
        Returns a dict describing the outcome:
        {
            "success": bool,
            "reason": str (if failed),
            "game_over": bool,
            "winner": symbol or None,
            "draw": bool
        }
        """
        if self.game_over:
            return {"success": False, "reason": "Game is already over."}
        if not self.board.is_valid_move(row, col):
            return {"success": False, "reason": "Cell is already taken."}
        self.board.make_move(row, col, self.current_symbol)
        self.move_history.append((self.current_symbol, row, col))
        winner = self.board.check_winner()
        if winner:
            self.game_over = True
            self.winner_symbol = winner
            return {"success": True, "game_over": True, "winner": winner, "draw": False}
        if self.board.is_full():
            self.game_over = True
            return {"success": True, "game_over": True, "winner": None, "draw": True}
        # Switch turns
        self.current_symbol = "O" if self.current_symbol == "X" else "X"
        return {"success": True, "game_over": False, "winner": None, "draw": False}
    def get_move_history(self):
        """Return the list of moves made so far."""
        return list(self.move_history)