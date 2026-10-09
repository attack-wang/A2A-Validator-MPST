'''
game.py
Defines the Game class: turn management, input validation and the
main loop that runs a Connect Four match until win or draw. The input
reading in prompt_column is guarded against closed or interrupted
streams (EOFError / KeyboardInterrupt), which are re-raised so the
entry point can shut down gracefully instead of crashing.
'''
from board import Board
from exceptions import ColumnFullError
from player import Player
class Game:
    """A two-player Connect Four match played in the terminal."""
    def __init__(self, player_one: Player, player_two: Player):
        """Create the board and let player_one move first."""
        self.board = Board()
        self.players = [player_one, player_two]
        self.current_index = 0
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self.players[self.current_index]
    def switch_turn(self):
        """Hand the turn over to the other player."""
        self.current_index = 1 - self.current_index
    def prompt_column(self):
        """Prompt the current player for a column number.
        Keeps asking until the input is an integer within 1..COLS and
        the column is not full. A closed (EOF) or interrupted input
        stream is re-raised so the caller can exit cleanly.
        Returns:
            int: the validated 1-based column number.
        """
        while True:
            try:
                raw = input(
                    f"{self.current_player}, choose a column "
                    f"(1-{self.board.COLS}): "
                ).strip()
            except (EOFError, KeyboardInterrupt):
                # Input stream closed or interrupted: propagate the
                # exception so the entry point can exit gracefully
                # instead of crashing with a traceback.
                print()
                raise
            try:
                column = int(raw)
            except ValueError:
                print("Invalid input - please enter a number.")
                continue
            if not self.board.is_valid_column(column):
                print(f"Out of range - column must be between 1 "
                      f"and {self.board.COLS}.")
                continue
            if self.board.column_is_full(column):
                print(f"Column {column} is already full - choose another.")
                continue
            return column
    def take_turn(self):
        """Drop the current player's disc into the chosen column.
        Returns:
            tuple: (row, col) zero-based coordinates of the placed disc.
        """
        while True:
            column = self.prompt_column()
            try:
                return self.board.drop_disc(column, self.current_player.disc)
            except ColumnFullError:
                # Defensive fallback; prompt_column already filters full
                # columns.
                print(f"Column {column} is already full - choose another.")
    def play(self):
        """Run the match until a player wins or the board fills up."""
        print("Connect Four - line up four discs to win!")
        print(self.board.render())
        print()
        while True:
            row, col = self.take_turn()
            disc = self.current_player.disc
            print()
            print(self.board.render())
            print()
            if self.board.check_win(row, col, disc):
                print(f"*** {self.current_player} wins! ***")
                return
            if self.board.is_full():
                print("*** Draw - the board is full. ***")
                return
            self.switch_turn()