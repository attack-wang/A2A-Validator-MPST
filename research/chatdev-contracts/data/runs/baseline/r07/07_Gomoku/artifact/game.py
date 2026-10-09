'''
Game controller module for the Gomoku game.
Contains the Game class, which manages turn alternation between the
black and white players, tracks the game state (playing, black wins,
white wins, draw) and connects the board logic with the GUI.
'''
from board import Board
class Game:
    """Controls the flow and state of a single Gomoku match."""
    STATE_PLAYING = "playing"
    STATE_BLACK_WINS = "black_wins"
    STATE_WHITE_WINS = "white_wins"
    STATE_DRAW = "draw"
    def __init__(self, board_size=15):
        """Set up a new game; black always moves first."""
        self.board = Board(board_size)
        self.current_player = Board.BLACK
        self.state = self.STATE_PLAYING
        self.winning_line = None
        self.move_count = 0
    def reset(self):
        """Restart the match with an empty board; black moves first."""
        self.board.reset()
        self.current_player = Board.BLACK
        self.state = self.STATE_PLAYING
        self.winning_line = None
        self.move_count = 0
    @property
    def is_over(self):
        """Return True when the match has finished (win or draw)."""
        return self.state != self.STATE_PLAYING
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_player = (Board.WHITE if self.current_player == Board.BLACK
                               else Board.BLACK)
    def try_move(self, row, col):
        """Attempt to place a stone for the current player at (row, col).
        Returns True when the move was accepted. Updates the game state
        on a win or a draw, otherwise switches to the other player.
        """
        if self.is_over:
            return False
        if not self.board.place_stone(row, col, self.current_player):
            return False
        self.move_count += 1
        if self.board.check_win(row, col):
            self.winning_line = self.board.get_winning_line(row, col)
            self.state = (self.STATE_BLACK_WINS
                          if self.current_player == Board.BLACK
                          else self.STATE_WHITE_WINS)
        elif self.board.is_full():
            self.state = self.STATE_DRAW
        else:
            self.switch_player()
        return True
    def status_message(self):
        """Return a human-readable status line for the GUI."""
        if self.state == self.STATE_BLACK_WINS:
            return "Black wins! Press Restart to play again."
        if self.state == self.STATE_WHITE_WINS:
            return "White wins! Press Restart to play again."
        if self.state == self.STATE_DRAW:
            return "It's a draw! Press Restart to play again."
        return ("Black's turn" if self.current_player == Board.BLACK
                else "White's turn")