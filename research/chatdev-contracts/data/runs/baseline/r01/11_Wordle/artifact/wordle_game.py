'''Core Wordle game state machine.'''
from terminal_colors import GREEN, YELLOW, GREY
from validator import compute_feedback
MAX_ATTEMPTS = 6
WORD_LENGTH = 5
STATE_RANK = {GREY: 0, YELLOW: 1, GREEN: 2}
class WordleGame:
    def __init__(self, answer, max_attempts=MAX_ATTEMPTS):
        self.answer = answer.lower()
        self.max_attempts = max_attempts
        self.guesses = []
        self.feedbacks = []
        self.letter_states = {}
    @property
    def attempts_used(self):
        return len(self.guesses)
    @property
    def attempts_left(self):
        return self.max_attempts - self.attempts_used
    def is_won(self):
        return bool(self.guesses) and self.guesses[-1] == self.answer
    def is_finished(self):
        return self.is_won() or self.attempts_used >= self.max_attempts
    def make_guess(self, guess):
        """Record a validated guess; returns feedback list of states."""
        feedback = compute_feedback(guess, self.answer)
        self.guesses.append(guess)
        self.feedbacks.append(feedback)
        self._update_keyboard(guess, feedback)
        return feedback
    def _update_keyboard(self, guess, feedback):
        for letter, state in zip(guess, feedback):
            current = self.letter_states.get(letter)
            if current is None or STATE_RANK[state] > STATE_RANK[current]:
                self.letter_states[letter] = state