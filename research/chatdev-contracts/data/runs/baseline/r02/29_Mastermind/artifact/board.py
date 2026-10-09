'''
board.py
Stores the history of guesses and their feedback so the UI can
render the full board at any time.
'''
class Board:
    """Simple container for the guess history of one round."""
    def __init__(self):
        """Start with an empty board."""
        self.rows = []  # list of (guess, exact, partial) tuples
    def add_row(self, guess, exact, partial):
        """Append one guess and its feedback to the board."""
        self.rows.append((list(guess), exact, partial))