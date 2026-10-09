'''
feedback.py
...
'''
from collections import Counter
def compute_feedback(guess, secret):
    """Return (exact, partial)"""
    if len(guess) != len(secret):
        raise ValueError(...)
    exact = 0
    guess_rest = []
    secret_rest = []
    for g, s in zip(guess, secret):
        if g == s:
            exact += 1
        else:
            guess_rest.append(g)
            secret_rest.append(s)
    available = Counter(secret_rest)
    partial = 0
    for g in guess_rest:
        if available[g] > 0:
            partial += 1
            available[g] -= 1
    return exact, partial
def format_feedback(exact, partial, code_length):
    pegs = ["●"] * exact + ["○"] * partial + ["·"] * (code_length - exact - partial)
    return " ".join(pegs)