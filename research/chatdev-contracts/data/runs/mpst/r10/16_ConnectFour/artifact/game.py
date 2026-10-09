'''
game.py
Defines the Game class, which orchestrates a full Connect Four match:
it alternates turns between two players, reads and validates column
choices from the command line (robustly, so that unusual Unicode
digit characters can never crash the input loop), updates the board
after every move, and announces a win or a draw when the game ends.
'''
from board import Board
from player import Player
class Game:
    """Manages the turn-based flow of a Connect Four match."""
    QUIT_COMMANDS = ('q', 'quit', 'exit')
    def __init__(self, player_one=None, player_two=None):
        """Set up the board and the two players (defaults: X and O)."""
        self.board = Board()
        self.players = [
            player_one if player_one is not None else Player('Player 1', 'X'),
            player_two if player_two is not None else Player('Player 2', 'O'),
        ]
        self.current_index = 0
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self.players[self.current_index]
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_index = (self.current_index + 1) % len(self.players)
    def get_player_move(self):
        """Prompt the current player for a column until the choice is valid.
        Uses isdecimal() instead of isdigit() so that only characters
        int() is guaranteed to parse pass the guard (isdigit() accepts
        Unicode digits such as '²' that would make int() raise
        ValueError). A defensive try/except is kept as belt-and-braces.
        Returns the zero-based column index, or None if the player quits.
        """
        while True:
            prompt = (f"{self.current_player.name} ({self.current_player.disc}), "
                      f"choose a column 1-{self.board.cols} "
                      f"(or 'q' to quit): ")
            choice = input(prompt).strip().lower()
            if choice in Game.QUIT_COMMANDS:
                return None
            if not choice.isdecimal():  # isdecimal, not isdigit:
                print("Invalid input: please type a column number.")  # int() is guaranteed safe
                continue
            try:
                col = int(choice) - 1
            except ValueError:  # Defensive: isdecimal() should make this unreachable.
                print("Invalid input: please type a column number.")
                continue
            if not (0 <= col < self.board.cols):
                print(f"Out of range: column must be between 1 and {self.board.cols}.")
                continue
            if not self.board.is_valid_column(col):
                print("That column is already full. Choose another one.")
                continue
            return col
    def announce_result(self, winner):
        """Print the final message for a win or a draw."""
        print('\n' + '=' * 40)
        if winner is None:
            print("It's a draw! The board is full.")
        else:
            print(f"{winner.name} ({winner.disc}) connects four and wins!")
        print('=' * 40)
    def play(self):
        """Run the match until a win, a draw, or a quit.
        Returns True if the game reached a natural end (win or draw),
        False if a player quit early.
        """
        print('\nWelcome to Connect Four!')
        print(f"{self.players[0].name} uses '{self.players[0].disc}' and "
              f"{self.players[1].name} uses '{self.players[1].disc}'.")
        print("Connect four of your discs in a row to win.\n")
        self.board.display()
        while True:
            col = self.get_player_move()
            if col is None:
                print(f"\n{self.current_player.name} quit the game. Goodbye!")
                return False
            row = self.board.drop_disc(col, self.current_player.disc)
            self.board.display()
            if self.board.check_win(row, col, self.current_player.disc):
                self.announce_result(self.current_player)
                return True
            if self.board.is_full():
                self.announce_result(None)
                return True
            self.switch_player()