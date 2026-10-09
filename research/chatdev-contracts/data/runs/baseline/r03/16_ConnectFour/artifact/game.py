'''
Game module for the Connect Four game.
Defines the Game class, which orchestrates turn-taking, validates
player input, applies moves to the board, detects the outcome, and
announces the result.
'''
from board import Board
from exceptions import ColumnFullError, InvalidColumnError
from player import Player
class Game:
    """Manages the flow of a Connect Four match between two players."""
    DEFAULT_DISCS = ('X', 'O')
    def __init__(self, board=None, players=None):
        """Set up the board and the two players.
        Args:
            board: a Board instance; a fresh 6x7 board is created if omitted.
            players: a sequence of two Player instances; defaults are
                created with discs 'X' and 'O' if omitted.
        """
        self.board = board if board is not None else Board()
        if players is None:
            players = (
                Player("Player 1", self.DEFAULT_DISCS[0]),
                Player("Player 2", self.DEFAULT_DISCS[1]),
            )
        self.players = list(players)
        self.current_index = 0
        self.winner = None
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self.players[self.current_index]
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_index = (self.current_index + 1) % len(self.players)
    def get_valid_column(self, player):
        """Prompt the player until a valid, non-full column is entered.
        Accepts 1-based column numbers, re-printing an explanatory message
        for blank input, non-numeric input, out-of-range columns, and
        already-full columns.
        Returns:
            The 0-based column index ready for Board.drop_disc.
        """
        while True:
            raw = input(
                f"{player.name} ({player.disc}), choose a column "
                f"(1-{self.board.cols}): "
            ).strip()
            try:
                col = int(raw) - 1
            except ValueError:
                print("Please enter a number.")
                continue
            try:
                self.board.get_next_open_row(col)  # validation probe
            except InvalidColumnError:
                print(f"Column must be between 1 and {self.board.cols}.")
            except ColumnFullError:
                print(f"Column {col + 1} is full. Please choose another.")
            else:
                return col
    def announce_result(self):
        """Print the final board and the outcome of the match."""
        self.board.render()
        if self.winner is not None:
            print(f"{self.winner.name} ({self.winner.disc}) wins - four in a row!")
        else:
            print("It's a draw! The board is full.")
    def play(self):
        """Run the game loop until a player wins or the grid fills up."""
        print("=" * 24)
        print("     CONNECT FOUR")
        print("=" * 24)
        print(f"{self.players[0]} vs {self.players[1]}")
        print("Line up four discs horizontally, vertically, or diagonally to win.\n")
        while True:
            self.board.render()
            player = self.current_player
            col = self.get_valid_column(player)
            row, _ = self.board.drop_disc(col, player.disc)
            if self.board.check_win(row, col, player.disc):
                self.winner = player
                break
            if self.board.is_full():
                self.winner = None
                break
            self.switch_player()
        self.announce_result()