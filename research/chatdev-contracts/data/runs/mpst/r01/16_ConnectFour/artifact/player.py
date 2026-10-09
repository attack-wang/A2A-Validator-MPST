'''
player.py
Defines the Player class representing one Connect Four participant.
A player owns a name and a disc symbol ('X' or 'O') and is
responsible for reading their own column choice from the console,
re-prompting until the choice is a valid, non-full column. All stdin
reads go through ui.safe_input(), so a closed or exhausted input
stream ends the game cleanly instead of raising an unhandled EOFError.
'''
import ui
class Player:
    """A Connect Four player identified by a name and a disc symbol."""
    def __init__(self, name, disc):
        """Create a player with the given human-readable name and disc symbol."""
        self.name = name
        self.disc = disc
    def get_move(self, board):
        """Prompt until a valid column is chosen; return its 0-based index.
        The prompt loops until the typed value is an integer that
        points at a column which is inside the board and still has
        at least one empty cell. Input is read via ui.safe_input(),
        so EOF on stdin exits the program cleanly rather than
        crashing with an unhandled EOFError.
        """
        while True:
            raw = ui.safe_input(
                f"{self.name} ({self.disc}), choose a column "
                f"(1-{board.cols}): "
            ).strip()
            try:
                col = int(raw) - 1
            except ValueError:
                print(f"'{raw}' is not a number. Please type a column number.")
                continue
            if not board.is_valid_column(col):
                if 0 <= col < board.cols:
                    print(f"Column {col + 1} is already full. Choose another.")
                else:
                    print(f"Column must be between 1 and {board.cols}.")
                continue
            return col