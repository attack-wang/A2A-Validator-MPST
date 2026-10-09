'''Tracks score, lives, and overall game state.'''
from settings import SHIP_LIVES
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_WIN = "win"
class GameStats:
    '''Simple container for score, remaining lives, and game state.'''
    def __init__(self):
        self.reset()
    def reset(self):
        '''Reset score, lives, and state for a fresh game.'''
        self.score = 0
        self.lives = SHIP_LIVES
        self.state = STATE_PLAYING