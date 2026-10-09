import random
from feedback import calculate_feedback
from colors import COLOR_LETTERS
class MastermindGame:
    """State and rules for a single game of Mastermind."""
    def __init__(self, code_length=4, palette_size=6, max_attempts=10, seed=None):
        """
        Create a new game.
        code_length   - number of positions in the secret code
        palette_size  - how many distinct colors are available
        max_attempts  - number of guesses the player may make
        seed          - optional seed for reproducible codes (testing)
        """
        if not 2 <= code_length <= 8:
            raise ValueError("code_length must be between 2 and 8.")
        if not 3 <= palette_size <= len(COLOR_LETTERS):
            raise ValueError(
                f"palette_size must be between 3 and {len(COLOR_LETTERS)}."
            )
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1.")
        self.code_length = code_length
        self.palette_size = palette_size
        self.max_attempts = max_attempts
        self.palette = list(COLOR_LETTERS.keys())[:palette_size]
        self.secret = self._generate_secret_code(seed)
        self.attempts_used = 0
        self.history = []          # list of (guess_letters, exact, partial)
        self.won = False
        self.finished = False
    # ------------------------------------------------------------------
    # Setup helpers
    # ------------------------------------------------------------------
    def _generate_secret_code(self, seed=None):
        """Randomly build the hidden code (repeats allowed)."""
        rng = random.Random(seed)
        return [rng.choice(self.palette) for _ in range(self.code_length)]
    def palette_names(self):
        """Return (letter, color_name) pairs for the active palette."""
        return [(letter, COLOR_LETTERS[letter]) for letter in self.palette]
    # ------------------------------------------------------------------
    # Guess handling
    # ------------------------------------------------------------------
    def is_valid_guess(self, raw_guess):
        """
        Validate a raw guess string.
        Returns (is_valid, error_message); error_message is "" when valid.
        """
        guess = (raw_guess or "").strip().upper()
        if not guess:
            return False, "Empty input — please type a guess such as RGBY."
        if len(guess) != self.code_length:
            return False, (
                f"Guess must be exactly {self.code_length} letters "
                f"(you entered {len(guess)})."
            )
        invalid = sorted({ch for ch in guess if ch not in self.palette})
        if invalid:
            return False, (
                f"Invalid color letter(s): {', '.join(invalid)}. "
                f"Valid letters: {''.join(self.palette)}."
            )
        return True, ""
    def make_guess(self, raw_guess):
        """
        Submit a guess.
        Returns (exact, partial) feedback. Raises ValueError for invalid
        guesses and RuntimeError if the game is already over.
        """
        if self.finished:
            raise RuntimeError("The game is already over — start a new game.")
        valid, error = self.is_valid_guess(raw_guess)
        if not valid:
            raise ValueError(error)
        guess = [ch for ch in raw_guess.strip().upper()]
        exact, partial = calculate_feedback(self.secret, guess)
        self.attempts_used += 1
        self.history.append((guess, exact, partial))
        if exact == self.code_length:
            self.won = True
            self.finished = True
        elif self.attempts_used >= self.max_attempts:
            self.finished = True
        return exact, partial
    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------
    def is_won(self):
        """True when the player cracked the code."""
        return self.won
    def is_over(self):
        """True when the game has ended (win, loss, or forfeit)."""
        return self.finished
    def forfeit(self):
        """End the game early (player gave up)."""
        self.finished = True
    def remaining_attempts(self):
        """Number of guesses the player has left."""
        return self.max_attempts - self.attempts_used