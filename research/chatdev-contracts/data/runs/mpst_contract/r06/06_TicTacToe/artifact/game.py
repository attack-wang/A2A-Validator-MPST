"""Tic-tac-toe game logic module."""


class Board:
    """Standard 3x3 tic-tac-toe board that tracks moves and outcomes."""

    WIN_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6),             # diagonals
    ]

    def __init__(self):
        self.cells = [str(n) for n in range(1, 10)]

    def display(self):
        """Return a readable 3x3 grid showing cell numbers and marks."""
        lines = []
        for r in range(3):
            lines.append(" " + " | ".join(self.cells[r * 3:(r + 1) * 3]) + " ")
            if r < 2:
                lines.append("---+---+---")
        return "\n".join(lines)

    def is_valid_move(self, cell):
        """True if cell is a number 1-9 that has not been claimed."""
        return (cell.isdigit() and 1 <= int(cell) <= 9
                and self.cells[int(cell) - 1] not in ("X", "O"))

    def make_move(self, cell, player):
        """Place the player's mark on the chosen cell number."""
        self.cells[int(cell) - 1] = player

    def is_full(self):
        """True when every cell has been claimed by X or O."""
        return all(c in ("X", "O") for c in self.cells)

    def check_winner(self):
        """Return 'X' or 'O' if that player has three in a row, else None."""
        for a, b, c in self.WIN_LINES:
            if self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None