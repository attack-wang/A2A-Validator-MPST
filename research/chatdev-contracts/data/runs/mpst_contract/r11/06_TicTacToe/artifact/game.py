"""Tic-tac-toe game logic for a standard 3x3 grid."""


class Board:
    """Tracks moves on a 3x3 grid and determines the game outcome."""

    WIN_LINES = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6),             # diagonals
    )

    def __init__(self):
        self.cells = [str(n) for n in range(1, 10)]
        self.moves = []  # ordered history of (player, cell_number)

    def is_free(self, cell):
        return self.cells[cell] not in ("X", "O")

    def place(self, cell, player):
        if not 0 <= cell <= 8:
            raise ValueError("Choose a cell from 1 to 9.")
        if not self.is_free(cell):
            raise ValueError(f"Cell {cell + 1} is already taken.")
        self.cells[cell] = player
        self.moves.append((player, cell + 1))

    def winner(self):
        for a, b, c in self.WIN_LINES:
            if self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None

    def is_full(self):
        return all(c in ("X", "O") for c in self.cells)

    def render(self):
        sep = "\n---------\n"
        return sep.join(" | ".join(self.cells[i:i + 3]) for i in (0, 3, 6))