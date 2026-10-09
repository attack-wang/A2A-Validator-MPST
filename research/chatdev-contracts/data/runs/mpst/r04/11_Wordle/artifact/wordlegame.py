class WordleGame:
    def __init__(self, answer):
        self.answer = answer
        self.attempts = []
        self.max_attempts = MAX_ATTEMPTS
    def is_won(self): return self.attempts and self.attempts[-1] == self.answer
    def is_over(self): return self.is_won() or len(self.attempts) >= self.max_attempts
    def make_guess(self, guess): self.attempts.append(guess); return compute_feedback(guess, self.answer)