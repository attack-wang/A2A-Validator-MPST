"""Tic-tac-toe game logic: board state, move tracking, and win detection."""

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


class Board:
    """3x3 tic-tac-toe board that tracks each player's moves."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.cells = [" "] * 9
        self.history = []  # list of (mark, cell_number) in play order

    def is_free(self, pos):
        return self.cells[pos] == " "

    def place(self, pos, mark):
        self.cells[pos] = mark
        self.history.append((mark, pos + 1))

    def is_full(self):
        return " " not in self.cells

    def winner(self):
        """Return 'X' or 'O' if there is a winning line, else None."""
        for a, b, c in WIN_LINES:
            if self.cells[a] != " " and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None

    def render(self):
        """Return a friendly 3x3 grid; empty cells show their number."""
        rows = []
        for r in range(3):
            cells = []
            for c in range(3):
                i = r * 3 + c
                cells.append(str(i + 1) if self.cells[i] == " " else self.cells[i])
            rows.append(" " + " | ".join(cells) + " ")
            if r < 2:
                rows.append("---+---+---")
        return "\n".join(rows)