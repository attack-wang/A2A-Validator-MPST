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


class Minesweeper:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.flags_used = 0
        self.state = "playing"
        self.first_click = True
        self.board = [[Cell() for _ in range(cols)] for _ in range(rows)]

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
        safe = {(safe_r, safe_c)}
        safe.update(self.neighbors(safe_r, safe_c))
        spots = [(r, c) for r in range(self.rows) for c in range(self.cols)
                 if (r, c) not in safe]
        random.shuffle(spots)
        for r, c in spots[:self.mines]:
            self.board[r][c].mine = True
        for r in range(self.rows):
            for c in range(self.cols):
                self.board[r][c].adjacent = sum(
                    1 for nr, nc in self.neighbors(r, c)
                    if self.board[nr][nc].mine)

    def reveal(self, r, c):
        if self.state != "playing":
            return
        cell = self.board[r][c]
        if cell.revealed or cell.flagged:
            return
        if self.first_click:
            self.place_mines(r, c)
            self.first_click = False
        if cell.mine:
            self.state = "lost"
            for row in self.board:
                for other in row:
                    if other.mine:
                        other.revealed = True
            return
        self._flood(r, c)
        self._check_win()

    def _flood(self, r, c):
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            cell = self.board[cr][cc]
            if cell.revealed or cell.flagged or cell.mine:
                continue
            cell.revealed = True
            if cell.adjacent == 0:
                for nr, nc in self.neighbors(cr, cc):
                    if not self.board[nr][nc].revealed:
                        stack.append((nr, nc))

    def toggle_flag(self, r, c):
        if self.state != "playing":
            return
        cell = self.board[r][c]
        if cell.revealed:
            return
        cell.flagged = not cell.flagged
        self.flags_used += 1 if cell.flagged else -1

    def _check_win(self):
        if all(cell.revealed or cell.mine
               for row in self.board for cell in row):
            self.state = "won"

    def remaining_mines(self):
        return self.mines - self.flags_used