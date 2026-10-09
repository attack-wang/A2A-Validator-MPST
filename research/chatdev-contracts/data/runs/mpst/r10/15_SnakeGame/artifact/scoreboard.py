'''
scoreboard.py
Score tracking for the Classic Snake game.
Keeps the current score and an all-time high score that persists
across sessions in a small local file (highscore.txt).
'''
import os
HIGHSCORE_FILE = "highscore.txt"
class Scoreboard:
    """Current score plus persistent high score."""
    def __init__(self, points_per_food=1):
        self.points_per_food = points_per_food
        self.score = 0
        self.high_score = self._load_high_score()
    def reset(self, points_per_food=None):
        if points_per_food is not None:
            self.points_per_food = points_per_food
        self.score = 0
    def register_food_eaten(self):
        """Add points for one food item; returns the new score."""
        self.score += self.points_per_food
        return self.score
    @property
    def is_new_high_score(self):
        return self.score > self.high_score
    def finalize(self):
        """Update the stored high score if beaten and persist it."""
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score()
    def _load_high_score(self):
        try:
            with open(HIGHSCORE_FILE, "r", encoding="utf-8") as fh:
                return int(fh.read().strip() or 0)
        except (OSError, ValueError):
            return 0
    def _save_high_score(self):
        try:
            with open(HIGHSCORE_FILE, "w", encoding="utf-8") as fh:
                fh.write(str(self.high_score))
        except OSError:
            pass  # high score simply won't persist