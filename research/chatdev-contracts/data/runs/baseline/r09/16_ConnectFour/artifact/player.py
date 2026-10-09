'''
player.py
Defines the Player class: one participant, their disc symbol, and
validated input of their chosen column.
'''
class Player:
    """Holds a player's name and disc symbol, and reads their moves."""
    def __init__(self, name, disc):
        """Store the player's name and disc symbol ('X' or 'O')."""
        self.name = name
        self.disc = disc
    def get_move(self, board):
        """Prompt until the player enters a valid, non-full column.
        Accepts only integers in 1..board.columns; re-prompts on bad
        text, out-of-range numbers, or full columns. Returns the
        0-based column index. KeyboardInterrupt/EOFError propagate to
        main() for graceful exit.
        """
        while True:
            choice = input(
                f"{self.name} ({self.disc}), choose a column "
                f"(1-{board.columns}): "
            ).strip()
            if not choice.isdigit():
                print("Invalid input. Please type a number.")
                continue
            column = int(choice) - 1
            if not board.is_valid_column(column):
                print(f"Column must be between 1 and {board.columns}.")
                continue
            if not board.has_empty_slot(column):
                print("That column is full. Pick another one.")
                continue
            return column