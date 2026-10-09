'''
game.py
Core game logic for Gomoku (Five in a Row).
The Game class coordinates the Board and the two Players, enforces
turn order, applies moves, detects wins/draws, and supports restarting.
It is completely independent of the user interface, so both the GUI
and the console front-end can drive the same logic.
'''
from board import Board, BLACK, WHITE
from player import Player
# Possible game states
STATE_PLAYING = "playing"
STATE_BLACK_WINS = "black_wins"
STATE_WHITE_WINS = "white_wins"
STATE_DRAW = "draw"
class Game:
    """Manages one full Gomoku session (board, players, turns, result)."""
    def __init__(self, size=15, player1_name="Black", player2_name="White"):
        """
        Create a fresh game.
        :param size: board dimension (standard Gomoku uses 15).
        :param player1_name: display name of the player holding Black.
        :param player2_name: display name of the player holding White.
        """
        self.board = Board(size)
        self.players = [
            Player(player1_name, BLACK),
            Player(player2_name, WHITE),
        ]
        self.current_index = 0          # Black always moves first
        self.state = STATE_PLAYING
        self.winner = None              # Player object once the game is won
        self.last_move = None           # (row, col) of the most recent stone
    # ------------------------------------------------------------------ #
    # Properties
    # ------------------------------------------------------------------ #
    @property
    def current_player(self):
        """The player whose turn it is."""
        return self.players[self.current_index]
    @property
    def board_size(self):
        return self.board.size
    # ------------------------------------------------------------------ #
    # Move handling
    # ------------------------------------------------------------------ #
    def make_move(self, row, col):
        """
        Place the current player's stone at (row, col).
        :param row: zero-based row index.
        :param col: zero-based column index.
        :return: True  -> move accepted (the game may now be over),
                 False -> move rejected (out of bounds, occupied cell,
                          or the game has already finished).
        """
        if self.state != STATE_PLAYING:
            return False
        if not self.board.is_valid_move(row, col):
            return False
        stone = self.current_player.stone
        self.board.place_stone(row, col, stone)
        self.last_move = (row, col)
        if self.board.check_win(row, col, stone):
            self.state = STATE_BLACK_WINS if stone == BLACK else STATE_WHITE_WINS
            self.winner = self.current_player
        elif self.board.is_full():
            self.state = STATE_DRAW
        else:
            self.switch_player()
        return True
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_index = 1 - self.current_index
    # ------------------------------------------------------------------ #
    # State queries
    # ------------------------------------------------------------------ #
    def is_over(self):
        """True when the game has been won or drawn."""
        return self.state != STATE_PLAYING
    def is_draw(self):
        """True when the game ended without a winner."""
        return self.state == STATE_DRAW
    def reset(self):
        """Clear the board and restart the match with the same players."""
        self.board.reset()
        self.current_index = 0
        self.state = STATE_PLAYING
        self.winner = None
        self.last_move = None