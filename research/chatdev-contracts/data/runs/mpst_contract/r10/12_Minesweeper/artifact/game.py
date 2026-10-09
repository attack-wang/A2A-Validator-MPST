import random

DIFFICULTIES = {
    "Beginner": (9, 9, 10),
    "Intermediate": (16, 16, 40),
    "Expert": (30, 16, 99),
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
        self.mine_count = mines
        self.cells = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.first_move = True
        self.game_over = False
        self.won = False

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr or dc:
                    nr, nc = r + dr, c + dc
                    if self.in_bounds(nr, nc):
                        yield nr, nc

    def place_mines(self, safe_r, safe_c):
        safe = {(safe_r, safe_c)} | set(self.neighbors(safe_r, safe_c))
        spots = [(r, c) for r in range(self.rows) for c in range(self.cols)
                 if (r, c) not in safe]
        random.shuffle(spots)
        for r, c in spots[:self.mine_count]:
            self.cells[r][c].mine = True
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].adjacent = sum(
                    1 for nr, nc in self.neighbors(r, c)
                    if self.cells[nr][nc].mine)

    def reveal(self, r, c):
        if self.game_over:
            return
        cell = self.cells[r][c]
        if cell.revealed or cell.flagged:
            return
        if self.first_move:
            self.place_mines(r, c)
            self.first_move = False
        if cell.mine:
            cell.revealed = True
            self.game_over = True
            for row in self.cells:
                for cl in row:
                    if cl.mine:
                        cl.revealed = True
            return
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            cl = self.cells[cr][cc]
            if cl.revealed or cl.flagged:
                continue
            cl.revealed = True
            if cl.adjacent == 0:
                for nr, nc in self.neighbors(cr, cc):
                    if not self.cells[nr][nc].revealed:
                        stack.append((nr, nc))
        self.check_win()

    def toggle_flag(self, r, c):
        cell = self.cells[r][c]
        if not self.game_over and not cell.revealed:
            cell.flagged = not cell.flagged

    def check_win(self):
        if all(cl.revealed or cl.mine for row in self.cells for cl in row):
            self.won = True
            self.game_over = True
            for row in self.cells:
                for cl in row:
                    if cl.mine:
                        cl.flagged = True

    def flags_used(self):
        return sum(1 for row in self.cells for cl in row if cl.flagged)