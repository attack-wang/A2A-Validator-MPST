'''
board.py
Board model for Minesweeper: mine placement (with a safe first click),
adjacency computation, iterative flood-fill reveal, flagging and
win/lose bookkeeping.
'''
import random
from cell import Cell
class Board:
    def __init__(self, rows, cols, num_mines):
        total = rows * cols
        if num_mines >= total:
            num_mines = total - 1  # clamp degenerate configs
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.mines_placed = False
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
    def reset(self):
        for row in self.grid:
            for cell in row:
                cell.reset()
        self.mines_placed = False
    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols
    def get_cell(self, row, col):
        return self.grid[row][col]
    def get_neighbors(self, row, col):
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self.in_bounds(r, c):
                    neighbors.append((r, c))
        return neighbors
    def place_mines(self, safe_row, safe_col):
        safe_zone = {(safe_row + dr, safe_col + dc)
                     for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                     if self.in_bounds(safe_row + dr, safe_col + dc)}
        if self.num_mines > self.rows * self.cols - len(safe_zone):
            safe_zone = {(safe_row, safe_col)}
        candidates = [(r, c) for r in range(self.rows) for c in range(self.cols)
                      if (r, c) not in safe_zone]
        for r, c in random.sample(candidates, self.num_mines):
            self.grid[r][c].is_mine = True
        self.mines_placed = True
        self._compute_adjacency()
    def _compute_adjacency(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.is_mine:
                    cell.adjacent_mines = 0  # not used for mines
                    continue
                cell.adjacent_mines = sum(1 for nr, nc in self.get_neighbors(r, c) if self.grid[nr][nc].is_mine)
    def reveal_cell(self, row, col):
        if not self.in_bounds(row, col):
            return []
        cell = self.grid[row][col]
        if cell.is_flagged or cell.is_revealed:
            return []
        if not self.mines_placed:
            self.place_mines(row, col)
        if cell.is_mine:
            cell.reveal()
            cell.exploded = True
            return [cell]
        revealed = []
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            cur = self.grid[r][c]
            if cur.is_revealed or cur.is_flagged or cur.is_mine:
                continue
            cur.reveal()
            revealed.append(cur)
            if cur.adjacent_mines == 0:
                for nr, nc in self.get_neighbors(r, c):
                    if not self.grid[nr][nc].is_revealed:
                        stack.append((nr, nc))
        return revealed
    def toggle_flag(self, row, col):
        if not self.in_bounds(row, col):
            return False
        cell = self.grid[row][col]
        if cell.is_revealed:
            return False
        cell.toggle_flag()
        return True
    def count_flagged(self):
        return sum(1 for row in self.grid for cell in row if cell.is_flagged)
    def reveal_all_mines(self, exploded_pos):
        for row in self.grid:
            for cell in row:
                if cell.is_mine and not cell.is_flagged:
                    cell.reveal()
                    if (cell.row, cell.col) == exploded_pos:
                        cell.exploded = True
                elif not cell.is_mine and cell.is_flagged:
                    cell.wrong_flag = True
    def flag_all_mines(self):
        for row in self.grid:
            for cell in row:
                if cell.is_mine:
                    cell.is_flagged = True
    def check_win(self):
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True