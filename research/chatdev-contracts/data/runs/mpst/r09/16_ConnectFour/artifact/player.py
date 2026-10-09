'''
player.py
Defines the Player class for the Connect Four game. Each player has a
display name and a disc symbol (for example 'X' or 'O') used to mark
cells on the board.
'''
class Player:
    """Represents a Connect Four player identified by name and disc symbol."""
    def __init__(self, name, disc):
        """Initialize the player with a display name and a disc symbol."""
        self._name = name
        self._disc = disc
    @property
    def name(self):
        """Return the player's display name."""
        return self._name
    @property
    def disc(self):
        """Return the symbol used for this player's discs."""
        return self._disc
    def __str__(self):
        """Return a readable description of the player."""
        return "{} (disc '{}')".format(self._name, self._disc)