'''
player.py
Defines the Player class for the Reversi (Othello) game.
A player is identified by a name and the disc colour (BLACK or WHITE)
they place on the board.
'''
from board import BLACK, WHITE
class Player:
    '''Represents one of the two Reversi players.'''
    def __init__(self, name, disc):
        '''
        Create a player with the given name and disc colour.
        `disc` must be BLACK ('B') or WHITE ('W').
        '''
        if disc not in (BLACK, WHITE):
            raise ValueError("disc must be BLACK ('B') or WHITE ('W')")
        self.name = name
        self.disc = disc
    @property
    def opponent_disc(self):
        '''Return the disc colour used by the opposing player.'''
        return WHITE if self.disc == BLACK else BLACK
    def __str__(self):
        '''Return a readable description of the player.'''
        return f'{self.name} [{self.disc}]'