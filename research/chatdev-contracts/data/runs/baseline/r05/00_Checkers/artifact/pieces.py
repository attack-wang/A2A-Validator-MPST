'''
pieces.py
Defines the two players (RED and BLACK) and the checkers piece (man or king),
including movement direction and promotion row derived from the player.
'''
from enum import Enum
class Player(Enum):
    RED = 'r'
    BLACK = 'b'
    @property
    def direction(self):
        """Forward row direction: RED moves up (towards row 0), BLACK moves down."""
        return -1 if self == Player.RED else 1
    @property
    def promotion_row(self):
        """Row at which this player's men are crowned kings."""
        return 0 if self == Player.RED else 7
    @property
    def opponent(self):
        return Player.BLACK if self == Player.RED else Player.RED
    @property
    def name_title(self):
        """Human-readable player name."""
        return 'Red' if self == Player.RED else 'Black'
class Piece:
    __slots__ = ('player', 'is_king')
    def __init__(self, player, is_king=False):
        self.player = player
        self.is_king = is_king
    def crown(self):
        """Promote this man to a king."""
        self.is_king = True
    @property
    def symbol(self):
        """Lowercase for men, uppercase for kings; 'r'/'R' red, 'b'/'B' black."""
        base = self.player.value
        return base.upper() if self.is_king else base
    def __repr__(self):
        return f"Piece({self.player.name}, king={self.is_king})"