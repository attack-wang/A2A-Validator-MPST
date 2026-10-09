'''
player.py
Defines the Player class for the Connect Four game.
A Player holds a name and a disc symbol, and keeps asking for a
column until the user types a valid, non-full column number.
'''
class Player:
    """Represents one Connect Four player and handles their input."""
    def __init__(self, name, disc):
        """Store the player's name and disc symbol ('X' or 'O')."""
        self.name = name
        self.disc = disc
    def get_move(self, board):
        """Prompt until the user enters a valid, non-full column; return 0-based index."""
        while True:
            prompt = f"{self.name} ({self.disc}), choose a column (1-{board.columns}): "
            choice = input(prompt).strip()
            if not choice.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            column = int(choice) - 1
            if not board.is_valid_column(column):
                if 0 <= column < board.columns:
                    print(f"Column {column + 1} is full. Choose another column.")
                else:
                    print(f"Column must be between 1 and {board.columns}.")
                continue
            return column