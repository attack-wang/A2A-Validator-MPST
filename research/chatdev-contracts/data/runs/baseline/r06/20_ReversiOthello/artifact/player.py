'''
player.py
Simple data holder for one Reversi participant.
A Player carries a display name and a disc colour (Board.BLACK or
Board.WHITE) plus a few convenience properties used by the Game and
GUI layers.
'''
from board import Board
class Player:
    """One Reversi participant identified by name and disc colour."""
    def __init__(self, name, color):
        """Create a player with `name` playing the given disc `color`."""
        self.name = name
        self.color = color
    @property
    def color_name(self):
        """Human-readable colour: 'Black' or 'White'."""
        return "Black" if self.color == Board.BLACK else "White"
    @property
    def opponent_color(self):
        """The disc colour belonging to the opposing player."""
        return Board.WHITE if self.color == Board.BLACK else Board.BLACK
    def __str__(self):
        """Readable representation, e.g. 'Player 1 (Black)'."""
        return f"{self.name} ({self.color_name})"