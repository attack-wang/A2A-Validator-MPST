'''Word lists and daily word selection.'''
from datetime import date
ANSWER_WORDS_RAW = """..."""
EXTRA_WORDS_RAW = """..."""
def _parse(raw):
    """Split raw text into a sorted, de-duplicated list of 5-letter words."""
    return sorted({w.strip().lower() for w in raw.split() if len(w.strip()) == 5})
ANSWER_WORDS = _parse(ANSWER_WORDS_RAW)
VALID_GUESS_WORDS = _parse(ANSWER_WORDS_RAW + " " + EXTRA_WORDS_RAW)
WORDLE_EPOCH = date(2021, 6, 19)
def get_daily_word(today=None):
    """Return the deterministic daily answer (same word for everyone on a given date)."""
    today = today or date.today()
    day_number = (today - WORDLE_EPOCH).days
    if day_number < 0:
        day_number = 0
    if not ANSWER_WORDS:
        raise RuntimeError("Answer word list is empty — cannot select a daily word.")
    return ANSWER_WORDS[day_number % len(ANSWER_WORDS)]
def get_random_word(rng=None):
    """Return a random answer word (for practice mode)."""
    import random
    rng = rng or random
    if not ANSWER_WORDS:
        raise RuntimeError("Answer word list is empty — cannot select a random word.")
    return rng.choice(ANSWER_WORDS)