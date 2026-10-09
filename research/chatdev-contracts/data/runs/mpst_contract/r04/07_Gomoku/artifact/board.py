"""Board module for the Gomoku game."""


class Board:
    SIZE = 15
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __init__(self, size=SIZE):
        self.size = size
        self.grid = [[self.EMPTY] * size for _ in range(size)]

    def in_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def is_empty(self, row, col):
        return self.grid[row][col] == self.EMPTY

    def place(self, row, col, player):
        if not self.in_bounds(row, col) or not self.is_empty(row, col):
            return False
        self.grid[row][col] = player
        return True

    def check_win(self, row, col, player):
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for dr, dc in directions:
            count = 1
            for sign in (1, -1):
                r, c = row + dr * sign, col + dc * sign
                while self.in_bounds(r, c) and self.grid[r][c] == player:
                    count += 1
                    r += dr * sign
                    c += dc * sign
            if count >= 5:
                return True
        return False

    def is_full(self):
        return all(cell != self.EMPTY for row in self.grid for cell in row)

    def render(self):
        header = "   " + " ".join(f"{c + 1:2d}" for c in range(self.size))
        lines = [header]
        for r in range(self.size):
            cells = " ".join(f"{self._symbol(self.grid[r][c]):>2}" for c in range(self.size))
            lines.append(f"{r + 1:2d} {cells}")
        return "\n".join(lines)

    @staticmethod
    def _symbol(cell):
        if cell == Board.BLACK:
            return "X"
        if cell == Board.WHITE:
            return "O"
        return "."