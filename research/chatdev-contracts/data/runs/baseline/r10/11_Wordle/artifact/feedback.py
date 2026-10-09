'''
feedback.py
Implements Wordle's letter-evaluation rules (green/yellow/grey).
'''
from enum import Enum
from colors import GREEN, YELLOW, GREY, RESET
class Feedback(Enum):
    CORRECT = "correct"      # green: right letter, right position
    PRESENT = "present"      # yellow: right letter, wrong position
    ABSENT = "absent"        # grey: letter not in the word
def evaluate_guess(guess, answer):
    """Standard two-pass Wordle algorithm handling duplicate letters."""
    guess = guess.lower()
    answer = answer.lower()
    feedback = [Feedback.ABSENT] * len(guess)
    remaining = {}
    # Pass 1: mark greens, count unmatched answer letters.
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            feedback[i] = Feedback.CORRECT
        else:
            remaining[a] = remaining.get(a, 0) + 1
    # Pass 2: mark yellows while letters remain, else grey.
    for i, g in enumerate(guess):
        if feedback[i] == Feedback.CORRECT:
            continue
        if remaining.get(g, 0) > 0:
            feedback[i] = Feedback.PRESENT
            remaining[g] -= 1
    return feedback
def render_feedback(guess, feedback):
    """Return the colored row string for one guess."""
    color_map = {Feedback.CORRECT: GREEN, Feedback.PRESENT: YELLOW, Feedback.ABSENT: GREY}
    parts = []
    for letter, fb in zip(guess.upper(), feedback):
        parts.append(f"{color_map[fb]} {letter} {RESET}")
    return "".join(parts)