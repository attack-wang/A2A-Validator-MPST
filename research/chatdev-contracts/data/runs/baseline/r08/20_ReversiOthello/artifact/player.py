'''
player.py
Defines the Player class, which represents one of the two participants
in a Reversi game, holding the player's name and disc colour.
'''
from board import BLACK, WHITE
class Player:
    """Represents a Reversi player identified by a name and disc colour."""
    def __init__(self, name: str, color: int) -> None:
        """
        Create a player.
        :param name:  display name of the player
        :param color: disc colour, one of the constants BLACK or WHITE
        """
        if color not in (BLACK, WHITE):
            raise ValueError("Player colour must be BLACK or WHITE.")
        self.name: str = name
        self.color: int = color
    @property
    def symbol(self) -> str:
        """Single-character symbol used to draw this player's discs."""
        return "X" if self.color == BLACK else "O"
    def __str__(self) -> str:
        """Human-readable representation, e.g. 'Alice (X)'."""
        return f"{self.name} ({self.symbol})"