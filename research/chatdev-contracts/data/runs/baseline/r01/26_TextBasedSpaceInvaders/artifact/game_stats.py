'''
game_stats.py
Tracks game statistics: score, lives, wave, and game state.
'''
import settings
class GameStats:
    """Track statistics and game state for Space Invaders."""
    def __init__(self):
        self.reset_stats()
        self.game_active = False
        self.game_over = False
        self.victory = False
        self.high_score = 0
    def reset_stats(self):
        self.lives = settings.SHIP_LIMIT
        self.score = 0
        self.wave = 1