'''
player.py
Defines the Player class representing one participant of the match.
'''
class Player:
    """Represents a Connect Four player identified by name and disc symbol."""
    def __init__(self, name, disc):
        """Store the player's name and the disc symbol (e.g. 'X' or 'O')."""
        self.name = name
        self.disc = disc