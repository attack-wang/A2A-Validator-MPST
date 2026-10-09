# history.py
"""Guess history tracking and rendering."""
class GameHistory:
    def __init__(self):
        self._entries = []  # list of (attempt_number, guess, feedback)
    def add(self, attempt, guess, feedback):
        self._entries.append((attempt, list(guess), feedback))
    def __len__(self):
        return len(self._entries)
    def render(self, code_length, max_attempts):
        """Render the history as a formatted table."""
        ...