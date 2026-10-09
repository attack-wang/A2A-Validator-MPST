'''
player.py
Contains the Player class which stores a player's name and disc color.
'''
from board import Board
class Player:
    """Represents one of the two Reversi players."""
    def __init__(self, name, color):
        """
        Create a player.
        :param name:  Display name of the player (e.g. "Alice").
        :param color: Disc color, either Board.BLACK ('B') or Board.WHITE ('W').
        """
        self.name = name
        self.color = color
    @property
    def color_name(self):
        """Human readable color name ('Black' or 'White')."""
        return 'Black' if self.color == Board.BLACK else 'White'
    def __str__(self):
        return f"{self.name} ({self.color_name})"