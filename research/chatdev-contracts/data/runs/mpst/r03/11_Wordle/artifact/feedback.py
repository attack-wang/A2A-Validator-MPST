'''
board.py
Renders the Wordle game board as colored text rows for the terminal.
Robustness notes:
  - Rendering is decoupled from evaluation: it consumes semantic markers
    ("green"/"yellow"/"grey") produced by feedback.evaluate_guess and maps
    them to ANSI codes, so it works identically when colors are disabled.
  - The board never mutates rows after they are added, keeping history
    stable across screen refreshes.
'''
from feedback import ANSI, GREY, GREEN, YELLOW, RESET, WORD_LENGTH
class Board:
    """Holds guess history and renders it as a colored terminal grid."""
    def __init__(self, max_attempts=6):
        """Create a board with room for `max_attempts` guess rows."""
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1.")
        self.max_attempts = max_attempts
        self.rows = []
    def add_row(self, evaluated):
        """Append one evaluated guess: a list of (letter, marker) tuples."""
        if len(self.rows) >= self.max_attempts:
            raise RuntimeError("Board is full: cannot add more guess rows.")
        if len(evaluated) != WORD_LENGTH:
            raise ValueError("Each evaluated guess must contain 5 (letter, marker) pairs.")
        self.rows.append(list(evaluated))
    def _render_filled_row(self, row):
        """Render one evaluated guess row with ANSI colors."""
        cells = []
        for letter, marker in row:
            color = ANSI.get(marker, "")
            cells.append(f"[{color}{letter.upper()}{RESET}]")
        return " ".join(cells)
    def _render_empty_row(self):
        """Render a placeholder row for an attempt not yet used."""
        return " ".join("[ _ ]" for _ in range(WORD_LENGTH))
    def render(self):
        """Return the full board as a multi-line string."""
        lines = []
        used = len(self.rows)
        for row in self.rows:
            lines.append(self._render_filled_row(row))
        for _ in range(self.max_attempts - used):
            lines.append(self._render_empty_row())
        return "\n".join(lines)