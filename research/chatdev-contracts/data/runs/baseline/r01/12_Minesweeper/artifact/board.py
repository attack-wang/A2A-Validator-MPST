'''
board.py — Minesweeper board: mine placement, flood-fill reveal, flagging and win/loss state.
'''
import random
from cell import Cell
class Board:
    """Game board holding the cell grid, mine layout and all game rules."""
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.rows = difficulty.rows
        self.cols = difficulty.cols
        self.num_mines = difficulty.mines
        self.grid = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self.mines_placed = False
        self.game_over = False
        self.won = False
        self.revealed_count = 0
        self.flag_count = 0
        self.exploded_at = None  # (row, col) of the mine that was clicked
    def in_bounds(self, row, col):
        """Return True when (row, col) lies inside the board."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    def get_cell(self, row, col):
        """Return the Cell located at (row, col)."""
        return self.grid[row][col]
    def get_neighbors(self, row, col):
        """Yield the coordinates of the (up to) eight neighbours of (row, col)."""
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self.in_bounds(r, c):
                    yield r, c
    def place_mines(self, safe_row, safe_col):
        """Randomly place all mines, keeping the first-clicked cell (and, when
        possible, its whole neighbourhood) mine-free."""
        candidates = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        candidates.remove((safe_row, safe_col))
        safe_zone = set(self.get_neighbors(safe_row, safe_col))
        remaining = [pos for pos in candidates if pos not in safe_zone]
        if len(remaining) >= self.num_mines:
            candidates = remaining
        mine_positions = random.sample(candidates, self.num_mines)
        for r, c in mine_positions:
            self.grid[r][c].is_mine = True
        self.mines_placed = True
        self.calculate_adjacent_mines()
    def calculate_adjacent_mines(self):
        """Compute the adjacent-mine counter for every non-mine cell."""
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if not cell.is_mine:
                    cell.adjacent_mines = sum(
                        1 for nr, nc in self.get_neighbors(r, c)
                        if self.grid[nr][nc].is_mine
                    )
    def reveal_cell(self, row, col):
        """Reveal the cell at (row, col).
        The first reveal places the mines with a safe start. Revealing a mine
        loses the game; revealing an empty cell flood-fills its neighbourhood
        (iteratively, so large boards never hit the recursion limit).
        Returns True when any cell state changed.
        """
        if self.game_over:
            return False
        cell = self.get_cell(row, col)
        if cell.is_revealed or cell.is_flagged:
            return False
        if not self.mines_placed:
            self.place_mines(row, col)
        if cell.is_mine:
            cell.is_revealed = True
            self.revealed_count += 1
            self.game_over = True
            self.won = False
            self.exploded_at = (row, col)
            return True
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            current = self.grid[r][c]
            if current.is_revealed or current.is_flagged or current.is_mine:
                continue
            current.is_revealed = True
            self.revealed_count += 1
            if current.adjacent_mines == 0:
                for nr, nc in self.get_neighbors(r, c):
                    neighbour = self.grid[nr][nc]
                    if not neighbour.is_revealed and not neighbour.is_flagged:
                        stack.append((nr, nc))
        self._check_win()
        return True
    def toggle_flag(self, row, col):
        """Toggle a flag on an unrevealed cell; returns True when it changed."""
        if self.game_over:
            return False
        cell = self.get_cell(row, col)
        changed = cell.toggle_flag()
        if changed:
            self.flag_count += 1 if cell.is_flagged else -1
        return changed
    def _check_win(self):
        """Win when every non-mine cell is revealed; auto-flag remaining mines."""
        safe_total = self.rows * self.cols - self.num_mines
        if self.revealed_count >= safe_total:
            self.won = True
            self.game_over = True
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.grid[r][c]
                    if cell.is_mine and not cell.is_flagged:
                        cell.is_flagged = True
                        self.flag_count += 1
    def flags_remaining(self):
        """Mines minus placed flags, shown on the mine counter."""
        return self.num_mines - self.flag_count