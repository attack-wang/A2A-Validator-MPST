"""Tic-tac-toe game logic."""

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


class Board:
    def __init__(self):
        self.cells = [" "] * 9

    def display(self):
        b = self.cells
        print()
        print(f" {b[0]} | {b[1]} | {b[2]} ")
        print("---+---+---")
        print(f" {b[3]} | {b[4]} | {b[5]} ")
        print("---+---+---")
        print(f" {b[6]} | {b[7]} | {b[8]} ")
        print()

    def is_empty(self, pos):
        return self.cells[pos] == " "

    def place(self, pos, mark):
        self.cells[pos] = mark

    def is_full(self):
        return " " not in self.cells

    def winner(self):
        for a, b, c in WIN_LINES:
            if self.cells[a] != " " and self.cells[a] == self.cells[b] == self.cells[c]:
                return self.cells[a]
        return None