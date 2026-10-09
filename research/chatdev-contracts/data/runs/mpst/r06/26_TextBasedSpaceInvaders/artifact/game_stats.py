'''Game statistics: score, lives, remaining aliens and win/lose state.'''
from settings import Settings
class GameStats:
    '''Tracks the dynamic state of a game session.'''
    def __init__(self, settings: Settings):
        self.settings = settings
        self.high_score = 0
        self.reset_stats()
    def reset_stats(self):
        '''Reset all per-game values while keeping the high score.'''
        self.score = 0
        self.lives_left = self.settings.starting_lives
        self.aliens_left = 0
        self.game_active = False
        # None = not started yet, True = victory, False = defeat.
        self.game_won = None
    def register_game_end(self):
        '''Update the high score once a game has finished.'''
        if self.score > self.high_score:
            self.high_score = self.score