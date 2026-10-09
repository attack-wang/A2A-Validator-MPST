'''
player.py
Defines the Player class representing a Gomoku participant
identified by a name and a stone color (black or white).
'''
from constants import BLACK, WHITE
class Player:
    '''Represents a Gomoku player.'''
    def __init__(self, name, color):
        if color not in (BLACK, WHITE):
            raise ValueError("color must be 'black' or 'white'")
        self.name = name
        self.color = color
    @property
    def symbol(self):
        '''Unicode symbol used to render this player's stones.'''
        return '●' if self.color == BLACK else '○'
    def __str__(self):
        return f"{self.name} ({self.color})"