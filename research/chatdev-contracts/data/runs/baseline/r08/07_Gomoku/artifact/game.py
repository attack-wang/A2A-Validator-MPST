'''
game.py
Game controller for Gomoku. Manages turn alternation between the black
and white players, delegates moves to the Board model, tracks the game
state (ongoing / black wins / white wins / draw), and supports reset.
'''
from constants import (
    BLACK, WHITE,
    STATE_ONGOING, STATE_BLACK_WINS, STATE_WHITE_WINS, STATE_DRAW,
)
from board import Board
class Game:
    """Controls the flow of a Gomoku match: turns, moves, and state."""
    def __init__(self):
        """Create a new game with an empty board; black always moves first."""
        self.board = Board()
        self.current_player = BLACK
        self.state = STATE_ONGOING
        self.winning_cells = []
    @property
    def is_over(self):
        """Return True when the match has ended in a win or a draw."""
        return self.state != STATE_ONGOING
    def make_move(self, row, col):
        """
        Attempt to place a stone for the current player at (row, col).
        Returns True if the move was valid and applied; False otherwise.
        On success, updates the game state: detects a win or draw, or
        hands the turn over to the opponent.
        """
        if self.is_over:
            return False
        if not self.board.place_stone(row, col, self.current_player):
            return False
        winning_line = self.board.check_win(row, col, self.current_player)
        if winning_line:
            self.winning_cells = winning_line
            self.state = (
                STATE_BLACK_WINS if self.current_player == BLACK else STATE_WHITE_WINS
            )
        elif self.board.is_full():
            self.state = STATE_DRAW
        else:
            self.switch_player()
        return True
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_player = WHITE if self.current_player == BLACK else BLACK
    def reset(self):
        """Clear the board and restore the initial game state."""
        self.board.reset()
        self.current_player = BLACK
        self.state = STATE_ONGOING
        self.winning_cells = []