"""Core Minesweeper game logic: board, mines, reveal, flags, win/lose."""
import random

DIFFICULTIES = {
    "Beginner": (9, 9, 10),
    "Intermediate": (16, 16, 40),
    "Expert": (16, 30, 99),
}


class MinesweeperGame:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.reset()

    def reset(self):
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.revealed = [[False] * self.cols for _ in range(self.rows)]
        self.flagged = [[False] * self.cols for _ in range(self.rows)]
        self.mines_placed = False
        self.game_over = False
        self.won = False
        self.first_click = True

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    yield nr, nc

    def place_mines(self, safe_r, safe_c):
        """Place mines avoiding the 3x3 area around the first click."""
        safe = [(r, c) for r in range(self.rows) for c in range(self.cols)
                if not (abs(r - safe_r) <= 1 and abs(c - safe_c) <= 1)]
        for r, c in random.sample(safe, min(self.mines, len(safe))):
            self.board[r][c] = -1
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != -1:
                    self.board[r][c] = self.count_adjacent(r, c)
        self.mines_placed = True

    def count_adjacent(self, r, c):
        return sum(1 for nr, nc in self.neighbors(r, c) if self.board[nr][nc] == -1)

    def reveal(self, r, c):
        """Left-click action. Returns True if the board changed."""
        if self.game_over or self.flagged[r][c] or self.revealed[r][c]:
            return False
        if self.first_click:
            self.place_mines(r, c)
            self.first_click = False
        if self.board[r][c] == -1:
            self.revealed[r][c] = True
            self.game_over = True
            self.won = False
            return True
        self._flood_reveal(r, c)
        self.check_win()
        return True

    def _flood_reveal(self, r, c):
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            if self.revealed[cr][cc] or self.flagged[cr][cc]:
                continue
            self.revealed[cr][cc] = True
            if self.board[cr][cc] == 0:
                for nr, nc in self.neighbors(cr, cc):
                    if not self.revealed[nr][nc]:
                        stack.append((nr, nc))

    def toggle_flag(self, r, c):
        """Right-click action: flag/unflag a suspected mine."""
        if self.game_over or self.revealed[r][c]:
            return
        self.flagged[r][c] = not self.flagged[r][c]

    def check_win(self):
        hidden = sum(1 for r in range(self.rows) for c in range(self.cols)
                     if not self.revealed[r][c])
        if hidden == self.mines:
            self.won = True
            self.game_over = True
            for r in range(self.rows):
                for c in range(self.cols):
                    if not self.revealed[r][c]:
                        self.flagged[r][c] = True

    def flags_used(self):
        return sum(1 for row in self.flagged for f in row if f)