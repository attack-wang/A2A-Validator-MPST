'''
feedback.py
Feedback calculation for the Mastermind game.
`Feedback` stores the number of exact matches (right symbol in the
right position) and partial matches (right symbol in the wrong
position). `calculate_feedback` compares a guess against the secret
code with a two-pass algorithm so duplicate symbols are counted
correctly, exactly as in classic Mastermind rules.
'''
class Feedback:
    """Result of comparing one guess against the secret code."""
    def __init__(self, exact_matches, partial_matches):
        self.exact_matches = exact_matches
        self.partial_matches = partial_matches
    def is_win(self, code_length):
        """True when every position is an exact match."""
        return self.exact_matches == code_length
    def __str__(self):
        return f"Exact: {self.exact_matches}, Partial: {self.partial_matches}"
    def __repr__(self):
        return (f"Feedback(exact_matches={self.exact_matches}, "
                f"partial_matches={self.partial_matches})")
    def __eq__(self, other):
        if not isinstance(other, Feedback):
            return NotImplemented
        return (self.exact_matches == other.exact_matches
                and self.partial_matches == other.partial_matches)
def calculate_feedback(guess, secret_code):
    """
    Compare `guess` to `secret_code` and return a Feedback object.
    Pass 1 counts exact matches (same symbol, same position) and masks
    those positions. Pass 2 counts the remaining symbol overlap
    (multiset intersection) as partial matches, so duplicates in the
    secret code or the guess are never over-counted.
    """
    if len(guess) != len(secret_code):
        raise ValueError("Guess and secret code must have the same length.")
    exact = 0
    remaining_guess = []
    remaining_secret = []
    # Pass 1: exact matches
    for guess_symbol, secret_symbol in zip(guess, secret_code):
        if guess_symbol == secret_symbol:
            exact += 1
        else:
            remaining_guess.append(guess_symbol)
            remaining_secret.append(secret_symbol)
    # Pass 2: partial matches via multiset intersection
    partial = 0
    secret_counts = {}
    for symbol in remaining_secret:
        secret_counts[symbol] = secret_counts.get(symbol, 0) + 1
    for symbol in remaining_guess:
        if secret_counts.get(symbol, 0) > 0:
            partial += 1
            secret_counts[symbol] -= 1
    return Feedback(exact, partial)