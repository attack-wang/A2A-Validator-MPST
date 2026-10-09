'''Guess validation and Wordle feedback logic.'''
from collections import Counter
from terminal_colors import GREEN, YELLOW, GREY
def normalize_guess(raw):
    """Trim and lowercase raw user input."""
    return raw.strip().lower()
def validate_guess(raw, valid_words, word_length=5):
    """Return (normalized_guess, error_message); guess is None when invalid."""
    guess = normalize_guess(raw)
    if not guess:
        return None, "Empty input — please type a 5-letter word."
    if not guess.isalpha():
        return None, "Guess must contain only letters A–Z."
    if len(guess) != word_length:
        return None, f"Guess must be exactly {word_length} letters (you typed {len(guess)})."
    if guess not in valid_words:
        return None, f"'{guess.upper()}' is not in the word list."
    return guess, None
def compute_feedback(guess, answer):
    """Wordle-accurate feedback with duplicate-letter handling (two-pass)."""
    n = len(answer)
    feedback = [GREY] * n
    remaining = Counter(answer)
    for i in range(n):
        if guess[i] == answer[i]:
            feedback[i] = GREEN
            remaining[guess[i]] -= 1
    for i in range(n):
        if feedback[i] == GREEN:
            continue
        if remaining.get(guess[i], 0) > 0:
            feedback[i] = YELLOW
            remaining[guess[i]] -= 1
    return feedback