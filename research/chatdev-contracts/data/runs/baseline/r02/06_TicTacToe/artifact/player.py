'''
player.py
Player module for the Tic-Tac-Toe game.
Defines the Player class, which holds a player's name and symbol and is
responsible for reading and validating that player's moves from the console.
Move prompts use the centralized safe_input() helper so a closed or
exhausted standard input stream ends the game gracefully instead of
raising an unhandled EOFError.
'''
from io_utils import safe_input
class Player:
    """Represents one tic-tac-toe player (name, symbol, and move input)."""
    def __init__(self, name: str, symbol: str):
        """Store the player's name and board symbol ('X' or 'O')."""
        self.name = name
        self.symbol = symbol
    def get_move(self, board) -> tuple:
        """Prompt until the user enters a valid, unoccupied 'row,col' move.
        Input uses human-friendly 1-based coordinates; the returned tuple
        is converted to 0-based (row, col) for Board.make_move. Reading the
        move via safe_input() guarantees graceful termination on EOF.
        """
        while True:
            raw = safe_input(
                f"{self.name} ({self.symbol}), enter move as 'row,col' (1-3): "
            ).strip()
            parts = [p.strip() for p in raw.split(',')]
            if len(parts) != 2 or not all(p.isdigit() for p in parts):
                print("  Invalid format. Enter two numbers separated by a comma, e.g. 2,3")
                continue
            row, col = int(parts[0]) - 1, int(parts[1]) - 1
            if not (0 <= row <= 2 and 0 <= col <= 2):
                print("  Coordinates must be between 1 and 3.")
                continue
            if not board.is_cell_empty(row, col):
                print("  That cell is already taken. Choose an empty one.")
                continue
            return row, col