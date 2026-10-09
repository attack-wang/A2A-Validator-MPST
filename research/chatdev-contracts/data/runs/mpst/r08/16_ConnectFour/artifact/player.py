'''
player.py
Defines the Player class for the Connect Four game.
A Player holds a display name and a disc symbol ('X' or 'O') and is
responsible for reading the human player's column choice from the
console, re-prompting until a valid, non-full column is entered.
The numeric conversion is guarded by try/except ValueError so that
exotic Unicode "digit" characters (e.g. '²', '①') that satisfy
isdigit() but cannot be converted by int() are safely rejected
instead of crashing the game.
'''
class Player:
    """Represents one Connect Four participant and their console input."""
    def __init__(self, name, symbol):
        """Store the player's name and disc symbol."""
        self.name = name
        self.symbol = symbol
    def get_move(self, board):
        """Prompt until the player types a valid column number.
        Accepts only integer input in the range 1..board.cols and rejects
        full columns. Returns the zero-based column index. The int()
        conversion is wrapped in try/except ValueError so that any
        non-numeric input — including Unicode characters such as '²' or
        '①' that pass isdigit() but fail int() — is handled as a normal
        invalid-input re-prompt rather than an unhandled crash.
        """
        while True:
            prompt = "{}, choose a column (1-{}): ".format(self.name, board.cols)
            raw = input(prompt).strip()
            try:
                column = int(raw) - 1
            except ValueError:
                print("  Invalid input: please type a number between 1 and {}.".format(
                    board.cols))
                continue
            if not 0 <= column < board.cols:
                print("  Column {} is out of range: please type a number between 1 and {}.".format(
                    raw, board.cols))
                continue
            if not board.is_valid_column(column):
                print("  Column {} is full: please choose another column.".format(raw))
                continue
            return column