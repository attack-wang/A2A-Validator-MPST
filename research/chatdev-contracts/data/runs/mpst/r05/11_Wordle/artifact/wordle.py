class WordleGame:
    WORD_LENGTH = 5
    MAX_ATTEMPTS = 6
    def __init__(self, answer, max_attempts=6):
        self.answer = answer.upper()
        self.max_attempts = max_attempts
        self.guesses = []  # list of (guess, states)
        self._keyboard = {}  # letter -> LetterState (best)
    def submit_guess(self, guess) -> list[LetterState]:
        guess = guess.upper()
        states = evaluate_guess(guess, self.answer)
        self.guesses.append((guess, states))
        update keyboard with max priority
        return states
    @property attempts_used
    def is_won(self): return any(g == self.answer for g,_ in self.guesses)
    def is_finished(self): return self.is_won or len(self.guesses) >= self.max_attempts
    def remaining_attempts(self)
    def render_board(colors_enabled, show_empty=True)
    def render_keyboard(colors_enabled)