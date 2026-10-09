'''
game.py
Defines the Game class, the controller that ties the Board and the two
Players together. It owns the turn order, applies moves, tracks the
current state, and records who won (or whether the round was a draw).
'''
from board import Board
from player import Player
class Game:
    """Coordinates turn-taking and win/draw detection for one round."""
    def __init__(self, player_x_name="Player 1", player_o_name="Player 2"):
        """
        Start a new round.
        Args:
            player_x_name (str): name of the player who moves first (X).
            player_o_name (str): name of the player who moves second (O).
        """
        self.board = Board()
        self.players = (Player(player_x_name, "X"), Player(player_o_name, "O"))
        self.current_index = 0          # index into self.players
        self.status = "ongoing"         # "ongoing" | "win" | "draw"
        self.winner = None              # Player object when status == "win"
        self.winning_line = None        # tuple of winning cell indices
    @property
    def current_player(self):
        """Return the Player whose turn it is."""
        return self.players[self.current_index]
    def switch_player(self):
        """Pass the turn to the other player."""
        self.current_index = 1 - self.current_index
    def play_move(self, index):
        """
        Attempt the current player's move in cell `index`.
        The move is rejected when the round is already finished or the
        cell is occupied. After a successful move the state is re-evaluated;
        the turn only switches while the round is still ongoing.
        Returns:
            bool: True if the move was applied, False otherwise.
        """
        if self.status != "ongoing":
            return False
        if not self.board.make_move(index, self.current_player.symbol):
            return False
        status, _symbol, line = self.board.check_winner()
        self.status = status
        if status == "win":
            self.winner = self.current_player
            self.winning_line = line
        elif status == "draw":
            self.winner = None
        else:
            self.switch_player()
        return True
    def is_over(self):
        """Return True when the round has been won or drawn."""
        return self.status in ("win", "draw")
    def reset(self):
        """Clear the board and restore the initial turn/state."""
        self.board.reset()
        self.current_index = 0
        self.status = "ongoing"
        self.winner = None
        self.winning_line = None