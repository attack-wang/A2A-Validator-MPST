'''
game.py
Defines the Game class that controls the flow of a Gomoku match:
turn management, move processing and game state tracking.
'''
from board import Board
class Game:
    """Controller for a two-player Gomoku game."""
    STATE_PLAYING = "playing"
    STATE_WON = "won"
    STATE_DRAW = "draw"
    PLAYER_NAMES = {Board.BLACK: "Black", Board.WHITE: "White"}
    def __init__(self, board_size=15):
        """Create a new game with an empty board; black always moves first."""
        self.board = Board(board_size)
        self.current_player = Board.BLACK
        self.state = self.STATE_PLAYING
        self.winner = None
        self.winning_line = []
        self.last_move = None
        self.move_count = 0
    def reset(self):
        """Start a fresh game."""
        self.board.reset()
        self.current_player = Board.BLACK
        self.state = self.STATE_PLAYING
        self.winner = None
        self.winning_line = []
        self.last_move = None
        self.move_count = 0
    @property
    def is_over(self):
        """True when the game has been won or ended in a draw."""
        return self.state != self.STATE_PLAYING
    def handle_move(self, row, col):
        """Attempt to play the current player's stone at (row, col).
        Returns True if the move was accepted, False otherwise.
        """
        if self.is_over or not self.board.is_valid_move(row, col):
            return False
        self.board.place_stone(row, col, self.current_player)
        self.last_move = (row, col)
        self.move_count += 1
        winning_line = self.board.check_win(row, col, self.current_player)
        if winning_line:
            self.state = self.STATE_WON
            self.winner = self.current_player
            self.winning_line = winning_line
        elif self.board.is_full():
            self.state = self.STATE_DRAW
        else:
            self.switch_player()
        return True
    def switch_player(self):
        """Alternate turns between black and white."""
        self.current_player = (Board.WHITE if self.current_player == Board.BLACK
                               else Board.BLACK)
    def get_status_text(self):
        """Human readable status line shown in the GUI."""
        if self.state == self.STATE_WON:
            return f"{self.PLAYER_NAMES[self.winner]} wins!"
        if self.state == self.STATE_DRAW:
            return "It's a draw!"
        return f"{self.PLAYER_NAMES[self.current_player]}'s turn"