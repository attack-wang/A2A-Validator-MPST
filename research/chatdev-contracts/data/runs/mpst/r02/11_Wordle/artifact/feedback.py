'''
feedback.py
Evaluation of a guess against the secret answer following standard
Wordle rules, including correct handling of duplicated letters.
'''
from enum import Enum
from collections import Counter
class Feedback(Enum):
    """Per-letter outcome of a guess."""
    CORRECT = "correct"    # right letter in the right position  -> green
    PRESENT = "present"    # right letter in the wrong position  -> yellow
    ABSENT = "absent"      # letter not in the answer            -> grey
def evaluate_guess(guess: str, answer: str) -> list:
    """Evaluate *guess* against *answer* and return per-letter Feedback list.
    Standard Wordle duplicate-letter rules:
      1. Positions where guess and answer letters match are CORRECT (green).
      2. Remaining letters are matched against the leftover multiset of the
         answer: each still-available letter yields PRESENT (yellow) at most
         as many times as it occurs in the answer outside green positions.
      3. Everything else is ABSENT (grey).
    """
    if len(guess) != len(answer):
        raise ValueError("guess and answer must have the same length")
    result = [Feedback.ABSENT] * len(answer)
    remaining = Counter(answer)
    for idx, (g_char, a_char) in enumerate(zip(guess, answer)):
        if g_char == a_char:
            result[idx] = Feedback.CORRECT
            remaining[g_char] -= 1
    for idx, g_char in enumerate(guess):
        if result[idx] is Feedback.CORRECT:
            continue
        if remaining.get(g_char, 0) > 0:
            result[idx] = Feedback.PRESENT
            remaining[g_char] -= 1
    return result