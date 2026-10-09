'''
ScoreBoard class for tracking and persisting high scores per difficulty.
'''
import json
import os
from config import SCORE_FILE
class ScoreBoard:
    '''Loads, records and saves high scores for each difficulty level.'''
    def __init__(self, filepath=SCORE_FILE):
        '''Initialize the scoreboard and load any existing scores.'''
        self.filepath = filepath
        self.high_scores = {}
        self.load()
    def load(self):
        '''Read high scores from disk, tolerating missing/corrupt files.'''
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    self.high_scores = {
                        str(k): int(v) for k, v in data.items()
                    }
            except (ValueError, OSError):
                self.high_scores = {}
    def save(self):
        '''Write high scores to disk.'''
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.high_scores, f, indent=2)
        except OSError:
            pass  # Persistence is best-effort; ignore write failures.
    def record_score(self, difficulty, score):
        '''Record a finished game; return True if it is a new high score.'''
        is_record = score > self.high_scores.get(difficulty, -1)
        if is_record:
            self.high_scores[difficulty] = score
            self.save()
        return is_record
    def get_high_score(self, difficulty):
        '''Return the stored high score for a difficulty (0 if none).'''
        return self.high_scores.get(difficulty, 0)