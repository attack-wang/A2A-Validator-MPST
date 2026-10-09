'''
player.py
Defines the Player class used by the Connect Four game.
A Player holds the display name and the disc symbol ('X' or 'O')
that identifies the player's pieces on the board.
'''
class Player:
    """Represents a Connect Four player identified by a disc symbol."""
    def __init__(self, name, disc):
        """Initialize a player with a display name and a disc symbol."""
        self._name = name
        self._disc = disc
    @property
    def name(self):
        """Return the player's display name."""
        return self._name
    @property
    def disc(self):
        """Return the disc symbol used to mark this player's moves."""
        return self._disc
    def __str__(self):
        """Return a human-friendly representation of the player."""
        return "{} ({})".format(self._name, self._disc)