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
    """Core Minesweeper logic: board state, reveals, flags, win/loss."""

    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.first_move = True
        self.game_over = False
        self.won = False
        self.flags_used = 0
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def neighbors(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    yield nr, nc

    def place_mines(self, safe_r, safe_c):
        safe = {(safe_r, safe_c)}
        safe.update(self.neighbors(safe_r, safe_c))
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
        """Uncover a cell; flood-fills zero regions. Returns changed cells."""
        if self.game_over:
            return []
        cell = self.grid[r][c]
        if cell.revealed or cell.flagged:
            return []
        if self.first_move:
            self.place_mines(r, c)
            self.first_move = False
        if cell.mine:
            cell.revealed = True
            self.game_over = True
            return [(r, c)]
        changed = []
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            cur = self.grid[cr][cc]
            if cur.revealed or cur.flagged or cur.mine:
                continue
            cur.revealed = True
            changed.append((cr, cc))
            if cur.adjacent == 0:
                for nr, nc in self.neighbors(cr, cc):
                    if not self.grid[nr][nc].revealed:
                        stack.append((nr, nc))
        self.check_win()
        return changed

    def toggle_flag(self, r, c):
        """Flag/unflag a hidden cell. Returns True if state changed."""
        if self.game_over:
            return False
        cell = self.grid[r][c]
        if cell.revealed:
            return False
        cell.flagged = not cell.flagged
        self.flags_used += 1 if cell.flagged else -1
        return True

    def check_win(self):
        if all(cell.revealed or cell.mine
               for row in self.grid for cell in row):
            self.won = True
            self.game_over = True
            for row in self.grid:
                for cell in row:
                    if cell.mine and not cell.flagged:
                        cell.flagged = True
                        self.flags_used += 1

    def mine_positions(self):
        return [(r, c) for r in range(self.rows) for c in range(self.cols)
                if self.grid[r][c].mine]