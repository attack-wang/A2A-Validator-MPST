'''
Persistent high score storage.
'''
import os
import settings
def load_high_score():
    '''Load the best score from disk; return 0 if missing or corrupted.'''
    try:
        with open(settings.HIGHSCORE_FILE) as f:
            value = int(f.read().strip())
        return value if value > 0 else 0
    except (FileNotFoundError, ValueError, OSError):
        return 0
def save_high_score(score):
    '''Persist the given score to disk as plain text.'''
    try:
        with open(settings.HIGHSCORE_FILE, "w") as f:
            f.write(str(max(0, int(score))))
    except OSError:
        pass