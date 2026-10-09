'''
player.py
Defines the Player class, which represents one tic-tac-toe participant.
Each player owns a symbol ("X" or "O") and a display name used by the UI.
'''
class Player:
    """Represents a single tic-tac-toe player."""
    def __init__(self, symbol, name):
        """
        Create a player.
        Args:
            symbol: The player's mark, must be "X" or "O".
            name:   Human-readable display name.
        """
        if symbol not in ("X", "O"):
            raise ValueError("Player symbol must be 'X' or 'O'.")
        self.symbol = symbol
        self.name = name
    def get_symbol(self):
        """Return this player's symbol ("X" or "O")."""
        return self.symbol
    def get_name(self):
        """Return this player's display name."""
        return self.name