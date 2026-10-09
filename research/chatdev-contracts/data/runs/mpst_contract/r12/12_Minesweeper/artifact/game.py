import random

DIFFICULTIES = {
    "Beginner": (9, 9, 10),
    "Intermediate": (16, 16, 40),
    "Expert": (16, 30, 99),
}


class Cell:
    __slots__ = ("mine", "revealed", "flagged", "adjacent")

    def __init__(self):
        self.mine = False
        self.revealed = False
        self.flagged = False
        self.adjacent = 0


class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.generated = False
        self.game_over = False
        self.won = False
        self.flags_used = 0

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    yield nr, nc

    def place_mines(self, safe_r, safe_c):
        safe = {(safe_r, safe_c)} | set(self.neighbors(safe_r, safe_c))
        spots = [(r, c) for r in range(self.rows) for c in range(self.cols)
                 if (r, c) not in safe]
        random.shuffle(spots)
        for r, c in spots[:self.mines]:
            self.grid[r][c].mine = True
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c].adjacent = sum(
                    1 for nr, nc in self.neighbors(r, c) if self.grid[nr][nc].mine)
        self.generated = True

    def reveal(self, r, c):
        if self.game_over:
            return
        cell = self.grid[r][c]
        if cell.revealed or cell.flagged:
            return
        if not self.generated:
            self.place_mines(r, c)
        cell.revealed = True
        if cell.mine:
            self.game_over = True
            for row in self.grid:
                for cl in row:
                    if cl.mine and not cl.flagged:
                        cl.revealed = True
            return
        if cell.adjacent == 0:
            for nr, nc in self.neighbors(r, c):
                if not self.grid[nr][nc].revealed:
                    self.reveal(nr, nc)
        self.check_win()

    def toggle_flag(self, r, c):
        cell = self.grid[r][c]
        if cell.revealed or self.game_over:
            return
        cell.flagged = not cell.flagged
        self.flags_used += 1 if cell.flagged else -1

    def check_win(self):
        if all(cl.revealed or cl.mine for row in self.grid for cl in row):
            self.won = True
            self.game_over = True