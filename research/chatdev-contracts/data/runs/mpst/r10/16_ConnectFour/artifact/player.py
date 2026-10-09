'''
player.py
Defines the Player class, which stores a Connect Four player's name
and the disc symbol ('X' or 'O') that marks their moves on the board.
'''
class Player:
    """Represents one of the two Connect Four players."""
    def __init__(self, name, disc):
        """Create a player with a display name and a one-character disc."""
        self.name = name
        self.disc = disc
    def __str__(self):
        """Return a readable description such as 'Player 1 (X)'."""
        return f"{self.name} ({self.disc})"