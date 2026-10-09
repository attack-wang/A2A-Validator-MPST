"""Core Minesweeper board logic: mines, reveal flood-fill, flags, win/lose."""
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
        self.mine_count = mines
        self.cells = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.mines_placed = False
        self.game_over = False
        self.won = False

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr or dc:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        yield nr, nc

    def place_mines(self, safe_r, safe_c):
        """Place mines after the first click, keeping the first click and its
        neighbors mine-free so the opening move is never an instant loss."""
        safe = {(safe_r, safe_c)} | set(self.neighbors(safe_r, safe_c))
        spots = [(r, c) for r in range(self.rows) for c in range(self.cols)
                 if (r, c) not in safe]
        for r, c in random.sample(spots, self.mine_count):
            self.cells[r][c].mine = True
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].adjacent = sum(
                    self.cells[nr][nc].mine for nr, nc in self.neighbors(r, c))
        self.mines_placed = True

    def reveal(self, r, c):
        """Uncover a cell; flood-fill zero-adjacency regions iteratively."""
        if self.game_over:
            return
        cell = self.cells[r][c]
        if cell.revealed or cell.flagged:
            return
        if not self.mines_placed:
            self.place_mines(r, c)
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            cur = self.cells[cr][cc]
            if cur.revealed or cur.flagged:
                continue
            cur.revealed = True
            if cur.mine:
                self.game_over = True
                return
            if cur.adjacent == 0:
                for nr, nc in self.neighbors(cr, cc):
                    if not self.cells[nr][nc].revealed:
                        stack.append((nr, nc))
        self.check_win()

    def toggle_flag(self, r, c):
        cell = self.cells[r][c]
        if not cell.revealed and not self.game_over:
            cell.flagged = not cell.flagged

    def check_win(self):
        if all(cell.revealed or cell.mine for row in self.cells for cell in row):
            self.won = True
            self.game_over = True
            for row in self.cells:
                for cell in row:
                    if cell.mine:
                        cell.flagged = True

    def flags_used(self):
        return sum(cell.flagged for row in self.cells for cell in row)