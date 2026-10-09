'''
player.py
This module defines the Player class, which represents a participant
in the Connect Four game, holding their name and disc symbol.
'''
class Player:
    """Represents a Connect Four player with a name and a disc symbol."""
    def __init__(self, name, disc):
        """Initialize the player with a display name and disc symbol."""
        self.name = name
        self.disc = disc
    def __str__(self):
        """Return a readable representation of the player."""
        return f"{self.name} ({self.disc})"