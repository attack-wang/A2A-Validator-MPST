'''
board.py
Pure game logic for Minesweeper, fully independent of any GUI toolkit.
Classes:
    CellState - enum of the three visual states of a cell
    Cell      - a single square of the minefield
    Board     - the grid plus all rules (mine placement, reveal flood-fill,
                flagging, chording, win/lose detection)
'''
import random
from enum import Enum
class CellState(Enum):
    COVERED = "covered"
    FLAGGED = "flagged"
    REVEALED = "revealed"
class Cell:
    """One square of the minefield."""
    __slots__ = ("is_mine", "adjacent_mines", "state")
    def __init__(self):
        self.is_mine = False
        self.adjacent_mines = 0
        self.state = CellState.COVERED
    @property
    def is_flagged(self):
        return self.state == CellState.FLAGGED
    @property
    def is_revealed(self):
        return self.state == CellState.REVEALED
class Board:
    """Grid of cells with all Minesweeper rules implemented."""
    def __init__(self, rows, cols, num_mines):
        if num_mines >= rows * cols:
            raise ValueError("Number of mines must be smaller than the board size")
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.cells = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.mines_placed = False
        self.game_over = False
        self.won = False
        self.flags_placed = 0
        self.revealed_safe = 0
        self.total_safe = rows * cols - num_mines
        self.exploded = None  # (row, col) of the mine that was hit
    # -- helpers -----------------------------------------------------------
    def in_bounds(self, row, col):
        """Return True if (row, col) lies inside the grid."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    def neighbors(self, row, col):
        """Yield the coordinates of the 8 surrounding in-bounds cells."""
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if self.in_bounds(nr, nc):
                    yield nr, nc
    # -- setup -------------------------------------------------------------
    def place_mines(self, safe_row, safe_col):
        """Randomly place mines, guaranteeing the first clicked cell (and
        preferably its neighbourhood) is mine-free."""
        excluded = {(safe_row, safe_col)}
        excluded.update(self.neighbors(safe_row, safe_col))
        candidates = [(r, c) for r in range(self.rows) for c in range(self.cols)
                      if (r, c) not in excluded]
        if len(candidates) < self.num_mines:
            candidates = [(r, c) for r in range(self.rows) for c in range(self.cols)
                          if (r, c) != (safe_row, safe_col)]
        for r, c in random.sample(candidates, self.num_mines):
            self.cells[r][c].is_mine = True
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.cells[r][c]
                if not cell.is_mine:
                    cell.adjacent_mines = sum(
                        1 for nr, nc in self.neighbors(r, c)
                        if self.cells[nr][nc].is_mine)
        self.mines_placed = True
    # -- player actions ------------------------------------------------------
    def reveal(self, row, col):
        """Uncover a cell. Returns 'ok', 'mine', 'win', or None if ignored."""
        if self.game_over or not self.in_bounds(row, col):
            return None
        cell = self.cells[row][col]
        if cell.is_flagged or cell.is_revealed:
            return None
        if not self.mines_placed:
            self.place_mines(row, col)  # first click is always safe
        if cell.is_mine:
            cell.state = CellState.REVEALED
            self.exploded = (row, col)
            self.game_over, self.won = True, False
            return "mine"
        self._flood_reveal(row, col)
        if self.is_won():
            self.game_over, self.won = True, True
            return "win"
        return "ok"
    def _flood_reveal(self, row, col):
        """Iterative flood-fill: reveal cell and, for zeros, expand outward."""
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            cell = self.cells[r][c]
            if cell.is_revealed or cell.is_flagged or cell.is_mine:
                continue
            cell.state = CellState.REVEALED
            self.revealed_safe += 1
            if cell.adjacent_mines == 0:
                for nr, nc in self.neighbors(r, c):
                    if not self.cells[nr][nc].is_revealed:
                        stack.append((nr, nc))
    def toggle_flag(self, row, col):
        """Flag/unflag a covered cell. Returns True if the board changed."""
        if self.game_over or not self.in_bounds(row, col):
            return False
        cell = self.cells[row][col]
        if cell.is_revealed:
            return False
        if cell.state == CellState.FLAGGED:
            cell.state = CellState.COVERED
            self.flags_placed -= 1
        else:
            cell.state = CellState.FLAGGED
            self.flags_placed += 1
        return True
    def chord(self, row, col):
        """Middle-click: if flags around a revealed number match it, reveal the rest."""
        if self.game_over or not self.in_bounds(row, col):
            return None
        cell = self.cells[row][col]
        if not cell.is_revealed or cell.adjacent_mines == 0:
            return None
        flagged = sum(1 for nr, nc in self.neighbors(row, col)
                      if self.cells[nr][nc].is_flagged)
        if flagged != cell.adjacent_mines:
            return None
        result = "ok"
        for nr, nc in list(self.neighbors(row, col)):
            n = self.cells[nr][nc]
            if not n.is_flagged and not n.is_revealed:
                res = self.reveal(nr, nc)
                if res == "mine":
                    result = "mine"
                elif res == "win" and result == "ok":
                    result = "win"
        return result
    # -- queries -----------------------------------------------------------
    def remaining_mines(self):
        """Mines minus flags (can go negative if too many flags placed)."""
        return self.num_mines - self.flags_placed
    def is_won(self):
        return self.revealed_safe == self.total_safe
    def mines(self):
        """List of (row, col) positions of every mine."""
        return [(r, c) for r in range(self.rows) for c in range(self.cols)
                if self.cells[r][c].is_mine]
    def wrong_flags(self):
        """List of (row, col) positions flagged although they hold no mine."""
        return [(r, c) for r in range(self.rows) for c in range(self.cols)
                if self.cells[r][c].is_flagged and not self.cells[r][c].is_mine]