'''
highscore.py
Persistent high-score storage for the Classic Snake game.
Stores a single integer in a small JSON file next to the game.
'''
import json
import settings
def load_highscore():
    """Return the stored high score, or 0 if the file is missing or corrupt."""
    try:
        with open(settings.HIGHSCORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return max(0, int(data.get("highscore", 0)))
    except (FileNotFoundError, ValueError, TypeError, json.JSONDecodeError):
        return 0
def save_highscore(score):
    """Persist the given high score; silently ignore write failures."""
    try:
        with open(settings.HIGHSCORE_FILE, "w", encoding="utf-8") as f:
            json.dump({"highscore": int(score)}, f)
    except OSError:
        pass