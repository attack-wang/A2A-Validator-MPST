"""Core Minesweeper logic: cells, board, difficulty presets."""
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
        self.rows, self.cols, self.mines = rows, cols, mines
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.started = False
        self.game_over = False
        self.won = False
        self.flags = 0
        self.revealed_count = 0
        self.hit = None

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr or dc:
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

    def reveal(self, r, c):
        if self.game_over:
            return
        cell = self.grid[r][c]
        if cell.revealed or cell.flagged:
            return
        if not self.started:
            self.started = True
            self.place_mines(r, c)
        if cell.mine:
            cell.revealed = True
            self.hit = (r, c)
            self.game_over = True
            self._reveal_all_mines()
            return
        self._flood(r, c)
        if self.revealed_count == self.rows * self.cols - self.mines:
            self.game_over = True
            self.won = True
            for row in self.grid:
                for mine_cell in row:
                    if mine_cell.mine and not mine_cell.flagged:
                        mine_cell.flagged = True
                        self.flags += 1

    def _flood(self, r, c):
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            cell = self.grid[cr][cc]
            if cell.revealed or cell.flagged or cell.mine:
                continue
            cell.revealed = True
            self.revealed_count += 1
            if cell.adjacent == 0:
                for nr, nc in self.neighbors(cr, cc):
                    if not self.grid[nr][nc].revealed:
                        stack.append((nr, nc))

    def toggle_flag(self, r, c):
        cell = self.grid[r][c]
        if self.game_over or cell.revealed:
            return
        cell.flagged = not cell.flagged
        self.flags += 1 if cell.flagged else -1

    def _reveal_all_mines(self):
        for row in self.grid:
            for cell in row:
                if cell.mine:
                    cell.revealed = True