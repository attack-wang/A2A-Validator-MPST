'''
storage.py
Tiny JSON-backed persistence layer for per-difficulty high scores.
'''
import json
import os
from settings import HIGH_SCORE_FILE
def load_high_scores():
    '''Load all high scores from disk; returns {} if missing/corrupt.'''
    if not os.path.exists(HIGH_SCORE_FILE):
        return {}
    try:
        with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return {k: int(v) for k, v in data.items() if isinstance(v, (int, float))}
    except (json.JSONDecodeError, OSError, ValueError):
        pass
    return {}
def save_high_score(difficulty, score):
    '''Persist score if it beats the stored best; return resulting best.'''
    scores = load_high_scores()
    best = max(int(scores.get(difficulty, 0)), int(score))
    scores[difficulty] = best
    try:
        with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2)
    except OSError:
        pass  # persistence is best-effort; never crash the game
    return best
def get_high_score(difficulty):
    '''Return the stored best score for ``difficulty`` (0 if none).'''
    return int(load_high_scores().get(difficulty, 0))
def reset_high_scores():
    '''Delete every stored high score.'''
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            os.remove(HIGH_SCORE_FILE)
    except OSError:
        pass