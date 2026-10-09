class GameEngine:
    def __init__(self, difficulty, rng=None):
        self.code_length = difficulty.code_length
        self.palette_size = difficulty.palette_size
        self.max_attempts = difficulty.max_attempts
        self.allow_duplicates = difficulty.allow_duplicates
        self.rng = rng or random.Random()
        self.secret = self._generate_secret()
        self.attempts_used = 0
    def _generate_secret(self):
        if self.allow_duplicates:
            return [self.rng.randrange(self.palette_size) for _ in range(self.code_length)]
        return self.rng.sample(range(self.palette_size), self.code_length)
    def evaluate_guess(self, guess): ...  # returns (exact, partial), increments attempts? 
    def is_win(self, guess): return guess == self.secret  # or exact == length