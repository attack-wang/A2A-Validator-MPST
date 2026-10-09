'''
game.py
Defines the Game class that orchestrates a complete Connect Four match.
The Game owns the Board and the two Players, alternates turns, applies
each move to the board, checks for a winning line or a full grid after
every move, and announces the final result.
'''
from board import Board
from player import Player
class Game:
    """Controls the turn-based flow of a two-player Connect Four game."""
    def __init__(self, player_one=None, player_two=None):
        """Set up the board, the two players, and the initial turn state."""
        self.board = Board()
        self.players = [
            player_one if player_one is not None else Player("Player 1", "X"),
            player_two if player_two is not None else Player("Player 2", "O"),
        ]
        self.current_index = 0
        self.winner = None
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self.players[self.current_index]
    def switch_turn(self):
        """Hand the turn over to the other player."""
        self.current_index = 1 - self.current_index
    def take_turn(self):
        """Run one turn: prompt for a move, drop the disc, and evaluate the outcome."""
        player = self.current_player
        column = player.get_move(self.board)
        row = self.board.drop_disc(column, player.symbol)
        self.board.display()
        if self.board.check_win(row, column, player.symbol):
            self.winner = player
        elif not self.board.is_full():
            self.switch_turn()
    def announce_result(self):
        """Print the winner or declare a draw."""
        if self.winner is not None:
            print("{} ({}) wins with four in a row!".format(
                self.winner.name, self.winner.symbol))
        else:
            print("It's a draw! The grid is full and no one connected four.")
    def play(self):
        """Run the main loop, alternating turns until a win or draw occurs."""
        print("Welcome to Connect Four!")
        print("Drop discs into columns 1-{}; first to connect four wins.".format(
            self.board.cols))
        self.board.display()
        while self.winner is None and not self.board.is_full():
            self.take_turn()
        self.announce_result()