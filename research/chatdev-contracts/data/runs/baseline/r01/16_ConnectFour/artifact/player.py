'''
player.py
Defines the Player class representing a Connect Four participant and
handles prompting for and validating the player's column choice. Input
is EOF-safe: when the input stream is closed or exhausted (EOFError)
or the user interrupts the program (KeyboardInterrupt), the game
aborts cleanly with a friendly message instead of crashing.
'''
import sys
class Player:
    """Represents one player and their disc symbol."""
    def __init__(self, name, disc):
        """Store the player's name and disc symbol ('X' or 'O')."""
        self.name = name
        self.disc = disc
    def get_move(self, board):
        """Prompt until a valid column is entered; return the 0-based index.
        Exits gracefully (status 0) if the input stream is closed or the
        program is interrupted, rather than raising an unhandled EOFError.
        """
        while True:
            prompt = "{}, choose a column (1-{}): ".format(self.name, board.COLUMNS)
            try:
                choice = input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                print("\nInput stream closed. Game aborted.")
                sys.exit(0)
            try:
                column = int(choice) - 1
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if not board.is_valid_column(column):
                if 0 <= column < board.COLUMNS:
                    print("Column {} is full. Pick another one.".format(column + 1))
                else:
                    print("Column must be between 1 and {}.".format(board.COLUMNS))
                continue
            return column