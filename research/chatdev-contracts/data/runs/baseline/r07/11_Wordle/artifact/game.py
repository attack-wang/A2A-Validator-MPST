'''
game.py
Core Wordle game state and rules.
WordleGame encapsulates:
- the secret answer and the set of valid guess words,
- the history of guesses with their per-letter feedback,
- attempt tracking (6 maximum),
- win/lose detection.
The class is pure logic (no I/O) so it can be unit-tested or reused
by other front-ends.
'''
from validator import Feedback, evaluate_guess, validate_guess
class WordleGame:
    MAX_ATTEMPTS = 6
    def __init__(self, answer, valid_words):
        self.answer = answer.lower()
        self.valid_words = set(valid_words)
        self.history = []  # list of (guess, [Feedback, ...]) tuples
    def attempts_used(self):
        return len(self.history)
    def attempts_remaining(self):
        return self.MAX_ATTEMPTS - self.attempts_used()
    def is_won(self):
        return bool(self.history) and self.history[-1][0] == self.answer
    def is_over(self):
        return self.is_won() or self.attempts_used() >= self.MAX_ATTEMPTS
    def submit_guess(self, raw_guess):
        """
        Validate and apply one guess.
        Returns (accepted: bool, payload):
          - if rejected, payload is an error message string (turn not consumed)
          - if accepted, payload is the list of Feedback for the guess
        """
        valid, error = validate_guess(raw_guess, self.valid_words)
        if not valid:
            return False, error
        guess = raw_guess.strip().lower()
        feedback = evaluate_guess(guess, self.answer)
        self.history.append((guess, feedback))
        return True, feedback
    def letter_states(self):
        """
        Aggregate the best-known state of each letter across all guesses,
        for rendering the on-screen keyboard.
        Returns dict letter -> Feedback (strongest state wins:
        CORRECT > PRESENT > ABSENT).
        """
        rank = {Feedback.ABSENT: 0, Feedback.PRESENT: 1, Feedback.CORRECT: 2}
        states = {}
        for guess, feedback in self.history:
            for letter, fb in zip(guess, feedback):
                current = states.get(letter)
                if current is None or rank[fb] > rank[current]:
                    states[letter] = fb
        return states