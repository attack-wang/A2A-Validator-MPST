"""
game_stats.py
Mutable state of a game session: current score, high score of this
session, remaining lives and flags describing the overall game state
(playing, won, lost). reset() restores the values of a fresh game.
"""
class GameStats:
    """Track score, lives and the overall state of the game."""
    def __init__(self, settings):
        self.settings = settings
        self.high_score = 0
        self.reset()
    def reset(self):
        """Restore the statistics of a brand new game."""
        self.score = 0
        self.lives_left = self.settings.STARTING_LIVES
        self.game_active = False    # a round is currently being played
        self.game_over = False      # the session has ended (win or lose)
        self.game_won = False       # the session ended with a victory
    def add_score(self, points):
        """Add points to the score and keep the high score up to date."""
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
    def lose_life(self):
        """Consume one life. Return True when no lives are left."""
        self.lives_left -= 1
        return self.lives_left <= 0