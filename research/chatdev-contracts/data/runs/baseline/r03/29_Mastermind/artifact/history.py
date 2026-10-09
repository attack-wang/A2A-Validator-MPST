'''
history.py
Tracks every guess made during a game and renders the board history.
'''
from ui import paint, paint_color_letter, render_pegs
from config import EMPTY_PEG
class GameHistory:
    """Stores (attempt, guess, feedback) triples and renders them as a table."""
    def __init__(self):
        self._entries = []
    def add(self, attempt_number, guess, feedback):
        self._entries.append((attempt_number, list(guess), feedback))
    def __len__(self):
        return len(self._entries)
    @property
    def entries(self):
        return list(self._entries)
    def render(self, code_length, max_attempts):
        """Return the full history as a formatted string (the game board)."""
        lines = []
        for attempt, guess, feedback in self._entries:
            guess_str = " ".join(paint_color_letter(letter) for letter in guess)
            lines.append(f"{attempt:>2}. {guess_str:<{code_length * 2 - 1}} | {render_pegs(feedback, code_length)}")
        for attempt in range(len(self._entries) + 1, max_attempts + 1):
            dots = " . ".join(["·"] * code_length)
            lines.append(f"{attempt:>2}. {dots} |")
        return "\n".join(lines)