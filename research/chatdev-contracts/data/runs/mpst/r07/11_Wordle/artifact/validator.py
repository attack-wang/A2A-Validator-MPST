'''
validator.py
Guess validation and Wordle feedback evaluation.
Responsible for two things:
1. Validating a raw guess (length, alphabet, dictionary membership)
   and producing a human-readable error message when invalid.
2. Evaluating a valid guess against the secret word and returning
   per-letter feedback using the official Wordle rules for
   duplicate letters (greens first, then yellows from the
   remaining letter counts).
'''
from colors import GREEN, YELLOW, GREY
WORD_LENGTH = 5
class GuessValidator:
    """Validates guesses and computes per-letter feedback."""
    def __init__(self, valid_words):
        # Store as an uppercase set for fast, case-insensitive lookups.
        self.valid_words = {word.upper() for word in valid_words}
    def is_valid_format(self, guess):
        """True if guess is exactly WORD_LENGTH alphabetic characters."""
        return len(guess) == WORD_LENGTH and guess.isalpha()
    def is_in_dictionary(self, guess):
        """True if the (uppercase) guess exists in the word list."""
        return guess.upper() in self.valid_words
    def validate(self, raw_guess):
        """
        Validate a raw guess string.
        Returns:
            (True, "") if the guess may be played,
            (False, error_message) otherwise.
        """
        guess = raw_guess.strip().upper()
        if not guess:
            return False, "Empty input — please type a 5-letter word."
        if not guess.isalpha():
            return False, "Guess may only contain letters A–Z."
        if len(guess) != WORD_LENGTH:
            return False, f"Guess must be exactly {WORD_LENGTH} letters (got {len(guess)})."
        if not self.is_in_dictionary(guess):
            return False, f"'{guess}' is not in the word list."
        return True, ""
    def evaluate(self, guess, target):
        """
        Compare `guess` to `target` and return a list of feedback codes,
        one per letter: GREEN, YELLOW or GREY.
        Implements the official duplicate-letter rule:
          - Pass 1: mark exact-position matches GREEN and count the
            leftover occurrences of each target letter.
          - Pass 2: for the remaining positions, mark YELLOW if the
            letter still has unused occurrences in the target,
            otherwise GREY.
        """
        guess = guess.upper()
        target = target.upper()
        feedback = [GREY] * WORD_LENGTH
        remaining = {}
        for i in range(WORD_LENGTH):
            if guess[i] == target[i]:
                feedback[i] = GREEN
            else:
                remaining[target[i]] = remaining.get(target[i], 0) + 1
        for i in range(WORD_LENGTH):
            if feedback[i] == GREEN:
                continue
            letter = guess[i]
            if remaining.get(letter, 0) > 0:
                feedback[i] = YELLOW
                remaining[letter] -= 1
            else:
                feedback[i] = GREY
        return feedback