'''Best-score persistence helpers.'''
BEST_FILE = "best_score.dat"
def load_best():
    """Read the best score from disk; return 0 if missing or corrupted."""
    try:
        with open(BEST_FILE) as f:
            return int(f.read().strip() or 0)
    except (IOError, ValueError):
        return 0
def save_best(score):
    """Write the best score to disk, ignoring write failures."""
    try:
        with open(BEST_FILE, "w") as f:
            f.write(str(score))
    except IOError:
        pass