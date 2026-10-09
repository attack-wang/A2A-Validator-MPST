'''
feedback.py
Evaluates a guess against the secret answer using standard Wordle rules,
including correct handling of duplicated letters, and produces colored
tiles for terminal rendering.
'''
from colors import GREEN, YELLOW, GREY
class Feedback:
    GREEN = "green"
    YELLOW = "yellow"
    GREY = "grey"
def evaluate_guess(guess, answer):
    """
    Compare guess to answer letter by letter.
    Returns a list of (letter, color_name) tuples.
    Standard Wordle duplicate handling:
      1. First pass: mark greens, count remaining occurrences of each answer letter.
      2. Second pass: mark yellows while remaining counts allow, otherwise grey.
    """
    result = [None] * len(guess)
    remaining = {}
    for g_char, a_char in zip(guess, answer):
        if g_char == a_char:
            result[...] = green
        else:
            remaining[a_char] = remaining.get(a_char, 0) + 1
    # second pass
    for i, g_char in enumerate(guess):
        if result[i] is not None: continue
        if remaining.get(g_char, 0) > 0:
            result[i] = (g_char, YELLOW)
            remaining[g_char] -= 1
        else:
            result[i] = (g_char, GREY)
    return result