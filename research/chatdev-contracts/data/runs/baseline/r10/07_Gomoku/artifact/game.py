'''
game.py
This module defines the GomokuGame class, which manages the flow of a
Gomoku match on top of the Board class.
Responsibilities:
* keeping track of whose turn it is (Black always moves first),
* accepting move requests from any user interface (console or GUI),
* applying valid moves and switching turns,
* detecting win and draw conditions after every move,
* remembering the winning line and the last move (for UI highlighting),
* supporting undo of the most recent move and full game resets.
'''
from board import Board, EMPTY, BLACK, WHITE, PLAYER_NAMES
class GomokuGame:
    """Turn management and rule enforcement for a two-player Gomoku game."""
    def __init__(self):
        self.board = Board()
        self.current_player = BLACK  # Black always opens the game.
        self.game_over = False
        self.winner = None           # Player constant, or None for a draw.
        self.winning_line = []       # Cells forming the winning five-in-a-row.
        self.last_move = None        # (row, col) of the most recent stone.
        self.move_history = []       # [(row, col, player), ...] in play order.
    def reset(self):
        """Start a brand new game with an empty board and Black to move."""
        self.board.reset()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None
        self.winning_line = []
        self.last_move = None
        self.move_history = []
    def play_move(self, row, col):
        """Attempt to place the current player's stone at (row, col).
        Returns True when the move was legal and applied, False otherwise.
        After a successful move the method checks for a win or a draw and,
        if the game continues, hands the turn over to the other player.
        """
        if self.game_over:
            return False
        if not self.board.is_valid_move(row, col):
            return False
        player = self.current_player
        self.board.place_stone(row, col, player)
        self.last_move = (row, col)
        self.move_history.append((row, col, player))
        winner = self.board.check_win(row, col)
        if winner is not None:
            self.game_over = True
            self.winner = winner
            self.winning_line = self.board.get_winning_line(row, col)
        elif self.board.is_full():
            self.game_over = True
            self.winner = None  # Board full with no five-in-a-row: draw.
        else:
            self.current_player = WHITE if player == BLACK else BLACK
        return True
    def undo_move(self):
        """Undo the most recent move.
        Returns True if a move was removed, False when the history is empty.
        The player who made the undone move is given the turn again.
        """
        if not self.move_history:
            return False
        row, col, player = self.move_history.pop()
        self.board.remove_stone(row, col)
        self.last_move = self.move_history[-1][:2] if self.move_history else None
        self.game_over = False
        self.winner = None
        self.winning_line = []
        self.current_player = player
        return True
    def get_status_message(self):
        """Return a human-readable description of the current game state."""
        if self.game_over:
            if self.winner is not None:
                return f"{PLAYER_NAMES[self.winner]} wins with five in a row!"
            return "The board is full - it's a draw!"
        return f"{PLAYER_NAMES[self.current_player]}'s turn"