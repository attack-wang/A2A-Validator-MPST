'''
highscore.py
Tiny persistence helpers for the best score (plain text file).
'''
from settings import HIGHSCORE_FILE
def load_high_score(path=HIGHSCORE_FILE):
    """Read the stored best score; return 0 if missing or corrupted."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except (OSError, ValueError):
        return 0
def save_high_score(score, path=HIGHSCORE_FILE):
    """Persist the best score; ignore write errors (e.g. read-only dir)."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(int(score)))
    except OSError:
        pass