'''
Player module for the Tic-Tac-Toe game.
This module defines the Player class, which represents one participant
(holding a name and a symbol, 'X' or 'O') and handles reading and
validating that player's move from the command line.
'''
class Player:
    """Represents a Tic-Tac-Toe player and their input handling."""
    def __init__(self, name, symbol):
        """Store the player's name and board symbol ('X' or 'O')."""
        self.name = name
        self.symbol = symbol
    def get_move(self, board):
        """Prompt the player for a move until a valid one is entered.
        The expected input format is 'row,column' using 1-based numbers,
        e.g. '1,3' for the top-right cell. Entering 'q' quits the round.
        Returns a (row, col) tuple with 0-based indices, or None if the
        player chose to quit.
        """
        while True:
            raw = input(
                f"{self.name} ({self.symbol}), enter your move as row,column "
                f"(e.g. 1,2) or 'q' to quit: "
            ).strip()
            if raw.lower() == "q":
                return None
            parts = raw.replace(" ", "").split(",")
            if len(parts) != 2:
                print("Invalid format. Please use 'row,column', for example 2,3.")
                continue
            try:
                row = int(parts[0]) - 1
                col = int(parts[1]) - 1
            except ValueError:
                print("Invalid input. Row and column must be numbers, e.g. 2,3.")
                continue
            if not (0 <= row < 3 and 0 <= col < 3):
                print("Out of range. Row and column must be between 1 and 3.")
                continue
            if not board.is_valid_move(row, col):
                print("That cell is already taken. Choose an empty cell.")
                continue
            return row, col