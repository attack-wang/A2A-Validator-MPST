'''
player.py
Defines the Player class used to represent a Connect Four participant.
'''
class Player:
    """A Connect Four player with a name and a disc symbol."""
    def __init__(self, name, disc):
        """Create a player.
        Args:
            name (str): display name of the player.
            disc (str): single-character board symbol, e.g. 'X' or 'O'.
        """
        self.name = name
        self.disc = disc
    def __str__(self):
        """Return a readable label such as 'Alice (X)'."""
        return f"{self.name} ({self.disc})"