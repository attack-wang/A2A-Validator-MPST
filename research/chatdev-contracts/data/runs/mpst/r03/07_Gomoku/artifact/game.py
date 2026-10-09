'''
game.py
Game controller for Gomoku. Manages turn order, applies moves to the
board, detects wins and draws, and exposes the game state to the GUI.
'''
from constants import BLACK, WHITE
from board import Board
class Game:
    """Controls the flow of a two-player Gomoku game."""
    def __init__(self):
        """Create a new game with an empty board; Black always moves first."""
        self.board = Board()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.last_move = None
        self.move_count = 0
    @property
    def current_player_name(self):
        """Human-readable name of the player who must move next."""
        return "Black" if self.current_player == BLACK else "White"
    def make_move(self, row, col):
        """
        Attempt to place the current player's stone at (row, col).
        Returns True if the move was applied. Handles win detection,
        draw detection, and turn switching.
        """
        if self.game_over:
            return False
        if not self.board.place_stone(row, col, self.current_player):
            return False
        self.last_move = (row, col)
        self.move_count += 1
        winning_line = self.board.get_winning_line(row, col)
        if winning_line is not None:
            self.game_over = True
            self.winner = self.current_player
            self.winning_line = winning_line
            return True
        if self.board.is_full():
            self.game_over = True
            self.winner = None  # Draw
            return True
        self.switch_player()
        return True
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_player = WHITE if self.current_player == BLACK else BLACK
    def reset(self):
        """Restore the game to its initial state."""
        self.board.reset()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.last_move = None
        self.move_count = 0