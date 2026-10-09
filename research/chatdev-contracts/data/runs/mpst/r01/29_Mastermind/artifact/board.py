'''
board.py
Renders the game board: palette legend, guess history with feedback pegs,
and the secret-reveal line shown at the end of a round.
'''
from feedback import format_feedback, EXACT_PEG, PARTIAL_PEG
from terminal_colors import colorize, style_peg, BOLD, RESET
class Board:
    """Collects guesses and renders the current state of the board."""
    def __init__(self, palette, code_length, max_attempts):
        self.palette = palette
        self.code_length = code_length
        self.max_attempts = max_attempts
        self.rows = []  # list of (guess_labels, exact, partial)
    def add_row(self, guess, exact, partial):
        """Store one played guess together with its peg counts."""
        self.rows.append((list(guess), exact, partial))
    def _entry_for(self, label):
        for entry in self.palette:
            if entry["label"] == label:
                return entry
        return {"label": label, "ansi": ""}
    def cell_width(self):
        return max(len(entry["label"]) for entry in self.palette)
    def render_legend(self):
        width = self.cell_width()
        cells = [
            colorize(entry["label"].center(width), entry["ansi"])
            + f"={entry['letter']}"
            for entry in self.palette
        ]
        return "Palette: " + "   ".join(cells)
    def _render_pegs(self, exact, partial):
        pegs = []
        for symbol in format_feedback(exact, partial, self.code_length).split(" "):
            if symbol == EXACT_PEG:
                pegs.append(style_peg(symbol, "exact"))
            elif symbol == PARTIAL_PEG:
                pegs.append(style_peg(symbol, "partial"))
            else:
                pegs.append(style_peg(symbol, "empty"))
        return " ".join(pegs)
    def render_row(self, number, guess, exact, partial):
        width = self.cell_width()
        cells = " ".join(
            colorize(label.center(width), self._entry_for(label)["ansi"])
            for label in guess
        )
        pegs = self._render_pegs(exact, partial)
        return f"{number:>2}. {cells}  ->  {pegs}  (exact {exact}, partial {partial})"
    def render(self, secret=None):
        width = self.cell_width()
        lines = []
        header = (
            f"{'#':>2}. "
            + " ".join(["?" .center(width)] * self.code_length)
            + "   ->  feedback"
        )
        lines.append(BOLD + header + RESET)
        for i, (guess, exact, partial) in enumerate(self.rows, 1):
            lines.append(self.render_row(i, guess, exact, partial))
        remaining = self.max_attempts - len(self.rows)
        lines.append(f"Attempts used: {len(self.rows)}/{self.max_attempts} (remaining {remaining})")
        if secret is not None:
            cells = " ".join(
                colorize(label.center(width), self._entry_for(label)["ansi"])
                for label in secret
            )
            lines.append(BOLD + "Secret code: " + cells + RESET)
        return "\n".join(lines)