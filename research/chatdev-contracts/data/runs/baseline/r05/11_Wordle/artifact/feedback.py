'''
Guess evaluation and feedback rendering per standard Wordle rules.
'''
from enum import Enum
from colors import colorize, GREEN_BG, YELLOW_BG, GREY_BG, BOLD, RESET
class LetterResult(Enum):
    CORRECT = "correct"
    PRESENT = "present"
    ABSENT = "absent"
def evaluate_guess(guess, answer):
    if len(guess) != len(answer) or len(guess) != 5:
        raise ValueError("guess and answer must both be 5-letter words")
    results = [LetterResult.ABSENT] * 5
    remaining = {}
    for i, ch in enumerate(answer):
        if guess[i] == ch:
            results[i] = LetterResult.CORRECT
        else:
            remaining[ch] = remaining.get(ch, 0) + 1
    for i, ch in enumerate(guess):
        if results[i] == LetterResult.CORRECT:
            continue
        if remaining.get(ch, 0) > 0:
            results[i] = LetterResult.PRESENT
            remaining[ch] -= 1
    return results
def render_feedback(guess, results, use_color=True):
    if use_color:
        style_map = {
            LetterResult.CORRECT: GREEN_BG,
            LetterResult.PRESENT: YELLOW_BG,
            LetterResult.ABSENT: GREY_BG,
        }
        return "".join(colorize(ch.upper(), style_map[r]) for ch, r in zip(guess, results))
    marker_map = {
        LetterResult.CORRECT: "[G]",
        LetterResult.PRESENT: "[Y]",
        LetterResult.ABSENT: "[.]",
    }
    return "".join(f"{ch.upper()}{marker_map[r]}" for ch, r in zip(guess, results))