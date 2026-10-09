'''
player.py
Defines the Player class, a lightweight model that stores each player's
name and mark ("X" or "O") used throughout the game.
'''
class Player:
    """Represents one of the two tic-tac-toe players."""
    def __init__(self, name, symbol):
        """
        Create a player.
        Args:
            name (str): display name shown in the interface.
            symbol (str): the player's mark, must be "X" or "O".
        Raises:
            ValueError: if `symbol` is not "X" or "O".
        """
        if symbol not in ("X", "O"):
            raise ValueError("Player symbol must be 'X' or 'O'.")
        self.name = name
        self.symbol = symbol
    def __str__(self):
        """Return a readable description, e.g. 'Alice (X)'."""
        return f"{self.name} ({self.symbol})"