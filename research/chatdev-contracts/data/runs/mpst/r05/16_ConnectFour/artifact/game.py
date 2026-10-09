'''
game.py
Defines the Game class that drives a full Connect Four match.
The Game owns the Board and the two Players, alternates turns, reads
and validates column choices from the console, updates the board after
every move and stops when a player wins, the board fills up (draw) or
a player quits.
'''
from board import Board
from player import Player
class Game:
    """Manages the turn-based flow of a Connect Four match."""
    QUIT_COMMAND = "q"
    def __init__(self, player_one_name="Player 1", player_two_name="Player 2"):
        """Create the board, the two players and set the starting turn."""
        self.board = Board()
        self.players = [
            Player(player_one_name, "X"),
            Player(player_two_name, "O"),
        ]
        self.current_index = 0
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self.players[self.current_index]
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_index = 1 - self.current_index
    def get_player_move(self, player):
        """
        Prompt the given player for a column number (1..cols).
        Keeps asking until the input is a valid, non-full column.
        Returns the 0-based column index, or None if the player quits
        or the input stream ends (EOF/Ctrl-C are treated as quitting).
        """
        while True:
            try:
                raw = input(
                    "{} ({}), choose a column 1-{} [{} = quit]: ".format(
                        player.name, player.disc, self.board.cols, self.QUIT_COMMAND
                    )
                ).strip().lower()
            except (EOFError, KeyboardInterrupt):
                print()
                return None
            if raw == self.QUIT_COMMAND:
                return None
            try:
                choice = int(raw)
            except ValueError:
                print("Invalid input: please type a number between 1 and {}.".format(
                    self.board.cols))
                continue
            col = choice - 1
            if not self.board.is_valid_column(col):
                if 0 <= col < self.board.cols:
                    print("Column {} is already full. Pick another one.".format(choice))
                else:
                    print("Column {} is out of range. Pick a number between 1 and {}.".format(
                        choice, self.board.cols))
                continue
            return col
    def play(self):
        """Run the match loop until a win, a draw or a quit occurs."""
        print("=== Connect Four ===")
        print("{} ({}) vs {} ({})".format(
            self.players[0].name, self.players[0].disc,
            self.players[1].name, self.players[1].disc,
        ))
        print("Take turns dropping discs into columns 1-{}.".format(self.board.cols))
        print("First to line up four discs horizontally, vertically or diagonally wins.\n")
        self.board.render()
        while True:
            player = self.current_player
            col = self.get_player_move(player)
            if col is None:
                print("\n{} forfeited the match. Goodbye!".format(player.name))
                return
            row, _ = self.board.drop_disc(col, player.disc)
            print("\n{} dropped a disc into column {}.".format(player.name, col + 1))
            self.board.render()
            if self.board.check_win(row, col, player.disc):
                print("\n{} ({}) wins with four in a row! Congratulations!".format(
                    player.name, player.disc))
                return
            if self.board.is_full():
                print("\nThe board is full - it's a draw!")
                return
            self.switch_player()