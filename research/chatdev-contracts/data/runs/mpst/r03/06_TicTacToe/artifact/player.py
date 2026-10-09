'''
player.py
Defines the Player class, which holds the identity and statistics of one
participant in the tic-tac-toe match.
Responsibilities:
    * Store the player's display name and board symbol ('X' or 'O').
    * Track how many rounds the player has won.
'''
class Player:
    """Represents a single tic-tac-toe player."""
    def __init__(self, name, symbol):
        """
        Args:
            name:   Human-readable player name shown in the UI.
            symbol: The mark the player places on the board ('X' or 'O').
        """
        if symbol not in ('X', 'O'):
            raise ValueError("Player symbol must be 'X' or 'O'.")
        self.name = name
        self.symbol = symbol
        self.wins = 0
    def record_win(self):
        """Increment this player's win counter after a victorious round."""
        self.wins += 1
    def reset_score(self):
        """Set the win counter back to zero."""
        self.wins = 0
    def __str__(self):
        return f"{self.name} ({self.symbol})"