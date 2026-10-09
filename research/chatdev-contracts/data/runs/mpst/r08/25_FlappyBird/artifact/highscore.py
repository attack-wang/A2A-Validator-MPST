'''
Persistent high-score storage (JSON file next to the game).
'''
import json
import os
HIGHSCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'highscore.json')
class HighScore:
    """Loads and saves the best score to a small JSON file."""
    def __init__(self, path=HIGHSCORE_FILE):
        self.path = path
    def load(self):
        """Return the stored best score, or 0 if missing/corrupt."""
        try:
            with open(self.path, 'r') as f:
                data = json.load(f)
            return max(0, int(data.get('best', 0)))
        except (IOError, OSError, ValueError, TypeError):
            return 0
    def save(self, score):
        """Persist the best score; failures are silently ignored."""
        try:
            with open(self.path, 'w') as f:
                json.dump({'best': int(score)}, f)
        except (IOError, OSError):
            pass