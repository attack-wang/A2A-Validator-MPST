'''
player.py
Defines the Player class used by the Connect Four game.
Each player has:
  * a display name (e.g. "Player 1"),
  * a single-character disc symbol (e.g. 'X' or 'O') used on the board.
'''
class Player:
    """Represents one participant in the Connect Four game."""
    def __init__(self, name, disc):
        """Initialise the player with a name and a disc symbol."""
        self.name = name
        self.disc = disc
    def __str__(self):
        """Readable representation, e.g. 'Player 1 (X)'."""
        return f"{self.name} ({self.disc})"