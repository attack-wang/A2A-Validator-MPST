'''
player.py
Player model for Gomoku.
A Player bundles the display name with the stone colour (BLACK or WHITE)
that the player uses for the whole match.
'''
from board import BLACK, WHITE
class Player:
    """A Gomoku participant identified by name and stone colour."""
    def __init__(self, name, stone):
        """
        :param name:  human-readable display name.
        :param stone: BLACK or WHITE constant from board.py.
        """
        if stone not in (BLACK, WHITE):
            raise ValueError("stone must be either BLACK or WHITE")
        self.name = name
        self.stone = stone
    @property
    def stone_name(self):
        """Human-readable colour of this player's stones."""
        return "Black" if self.stone == BLACK else "White"
    def __str__(self):
        return f"{self.name} ({self.stone_name})"
    def __repr__(self):
        return f"Player(name={self.name!r}, stone={self.stone_name})"