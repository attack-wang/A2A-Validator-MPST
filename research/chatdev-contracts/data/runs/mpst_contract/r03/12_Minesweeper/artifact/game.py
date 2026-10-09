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


class MinesweeperGame:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.cells = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.first_move = True
        self.game_over = False
        self.won = False

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
        for r, c in random.sample(spots, min(self.mines, len(spots))):
            self.cells[r][c].mine = True
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].adjacent = sum(
                    self.cells[nr][nc].mine for nr, nc in self.neighbors(r, c))

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
            return
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            cl = self.cells[cr][cc]
            if cl.revealed or cl.flagged or cl.mine:
                continue
            cl.revealed = True
            if cl.adjacent == 0:
                for nr, nc in self.neighbors(cr, cc):
                    if not self.cells[nr][nc].revealed:
                        stack.append((nr, nc))
        self.check_win()

    def toggle_flag(self, r, c):
        if self.game_over:
            return
        cell = self.cells[r][c]
        if not cell.revealed:
            cell.flagged = not cell.flagged

    def reveal_all_mines(self):
        for row in self.cells:
            for cell in row:
                if cell.mine:
                    cell.revealed = True

    def check_win(self):
        if all(cell.revealed or cell.mine for row in self.cells for cell in row):
            self.game_over = True
            self.won = True

    def flags_used(self):
        return sum(cell.flagged for row in self.cells for cell in row)