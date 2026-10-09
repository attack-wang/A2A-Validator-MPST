'''
player.py
This module defines the Player class, which represents a Gomoku
participant (Black or White). It contains no GUI or game-flow code,
so importing it from game.py creates no circular dependency.
'''
from board import Board
class Player:
    """Represents a Gomoku player identified by name and stone color."""
    def __init__(self, name, stone):
        """Initialize the player with a name and stone color
        (Board.BLACK or Board.WHITE)."""
        if stone not in (Board.BLACK, Board.WHITE):
            raise ValueError("stone must be Board.BLACK or Board.WHITE")
        self.name = name
        self.stone = stone
    @property
    def stone_name(self):
        """Return the human-readable color name ('Black' or 'White')."""
        return "Black" if self.stone == Board.BLACK else "White"
    def __str__(self):
        """Return a readable representation, e.g. 'Player 1 (Black)'."""
        return f"{self.name} ({self.stone_name})"