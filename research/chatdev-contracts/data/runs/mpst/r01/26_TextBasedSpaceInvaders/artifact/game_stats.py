'''game_stats.py: tracks score, high score, lives and level.'''
class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.high_score = self._load_high_score()
        self.reset()
    def reset(self):
        self.score = 0
        self.lives = self.settings.ship_limit
        self.level = 1
    def add_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score()
    def _load_high_score(self):
        try:
            with open('high_score.txt') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
    def _save_high_score(self):
        try:
            with open('high_score.txt', 'w') as f:
                f.write(str(self.high_score))
        except OSError:
            pass