"""
player.py
Player representation for the Reversi (Othello) game.
"""
from board import BLACK, WHITE, COLOR_NAMES
class Player:
    """A Reversi player identified by a colour and a display name."""
    def __init__(self, color, name=None):
        if color not in (BLACK, WHITE):
            raise ValueError("Player colour must be BLACK or WHITE")
        self.color = color
        self.name = name or COLOR_NAMES[color]
    @property
    def opponent_color(self):
        return 3 - self.color
    def __repr__(self):
        return f"Player(color={self.color}, name={self.name!r})"
    def __str__(self):
        return self.name