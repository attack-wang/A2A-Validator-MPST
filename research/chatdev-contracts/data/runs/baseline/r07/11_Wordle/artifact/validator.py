'''
validator.py
Guess validation and Wordle feedback evaluation.
- validate_guess(): checks a raw user input against the game rules
  (exactly five letters, alphabetic, must be a real word from the list).
- evaluate_guess(): computes per-letter feedback (green/yellow/grey)
  with correct handling of duplicate letters, mirroring official Wordle.
WORD_LENGTH is now imported from words.py so there is a single source
of truth for the required guess length (no circular import: words.py
depends only on the standard library).
'''
import re
from collections import Counter
from enum import Enum
from words import WORD_LENGTH
class Feedback(Enum):
    CORRECT = "correct"   # right letter, right position  -> green
    PRESENT = "present"   # right letter, wrong position  -> yellow
    ABSENT = "absent"     # letter not in the word        -> grey
_GUESS_PATTERN = re.compile(f"^[a-z]{{{WORD_LENGTH}}}$")
def validate_guess(guess, valid_words):
    """
    Validate a raw guess string.
    Returns (is_valid: bool, error_message: str or None).
    """
    guess = guess.strip().lower()
    if not guess:
        return False, "Empty input - please type a 5-letter word."
    if len(guess) != WORD_LENGTH:
        return False, f"Guess must be exactly {WORD_LENGTH} letters (you typed {len(guess)})."
    if not _GUESS_PATTERN.match(guess):
        return False, "Guess must contain only English letters a-z."
    if guess not in valid_words:
        return False, f"'{guess}' is not in the word list."
    return True, None
def evaluate_guess(guess, answer):
    """
    Compare guess to answer and return a list of Feedback, one per letter.
    Handles duplicate letters correctly:
      1. First mark all exact-position matches (green) and consume them.
      2. Then mark letters that still remain in the answer as yellow.
      3. Anything left over is grey.
    """
    feedback = [Feedback.ABSENT] * len(guess)
    remaining = Counter(answer)
    for i, (g_char, a_char) in enumerate(zip(guess, answer)):
        if g_char == a_char:
            feedback[i] = Feedback.CORRECT
            remaining[g_char] -= 1
    for i, g_char in enumerate(guess):
        if feedback[i] == Feedback.CORRECT:
            continue
        if remaining.get(g_char, 0) > 0:
            feedback[i] = Feedback.PRESENT
            remaining[g_char] -= 1
    return feedback