'''
game_logic.py
Core game logic for the Minesweeper game.
Contains the Cell model and the MinesweeperGame engine which handles
mine placement, cell revealing (with flood-fill), flagging and
win/lose detection. This module is completely independent from the
GUI so the rules can be tested on their own.
'''
import random
from config import GameConfig
# Possible states of the overall game.
STATE_PLAYING = "playing"
STATE_WON = "won"
STATE_LOST = "lost"
class Cell:
    """Represents a single square of the Minesweeper board."""
    __slots__ = ("is_mine", "is_revealed", "is_flagged",
                 "is_exploded", "adjacent_mines")
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.is_exploded = False  # True only for the mine that was clicked
        self.adjacent_mines = 0
    def reset(self):
        """Restore the cell to its initial hidden state."""
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.is_exploded = False
        self.adjacent_mines = 0
    def toggle_flag(self):
        """Flag/unflag the cell. Only hidden cells can be flagged."""
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
            return True
        return False
class MinesweeperGame:
    """Engine implementing the rules of Minesweeper."""
    def __init__(self, config: GameConfig):
        self.config = config
        self.rows = config.rows
        self.cols = config.cols
        self.mines = config.mines
        self.state = STATE_PLAYING
        self.board = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self.mines_placed = False
        self.flags_used = 0
        self.revealed_count = 0
    # ------------------------------------------------------------------
    # Board setup
    # ------------------------------------------------------------------
    def _neighbors(self, row, col):
        """Yield the coordinates of the (up to 8) neighbours of a cell."""
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    yield r, c
    def place_mines(self, safe_row, safe_col):
        """
        Randomly distribute the mines on the board.
        The first clicked cell and all of its neighbours are guaranteed
        to be mine-free so the opening move always uncovers something.
        """
        safe_cells = {(safe_row, safe_col)}
        safe_cells.update(self._neighbors(safe_row, safe_col))
        # All candidate positions (everything except the safe zone).
        candidates = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) not in safe_cells
        ]
        random.shuffle(candidates)
        mine_count = min(self.mines, len(candidates))
        for r, c in candidates[:mine_count]:
            self.board[r][c].is_mine = True
        self.mines = mine_count  # keep counters consistent with reality
        self._calculate_adjacent_mines()
        self.mines_placed = True
    def _calculate_adjacent_mines(self):
        """Compute the adjacent-mine counter of every cell."""
        for r in range(self.rows):
            for c in range(self.cols):
                count = 0
                for nr, nc in self._neighbors(r, c):
                    if self.board[nr][nc].is_mine:
                        count += 1
                self.board[r][c].adjacent_mines = count
    # ------------------------------------------------------------------
    # Player actions
    # ------------------------------------------------------------------
    def reveal_cell(self, row, col):
        """
        Reveal the cell at (row, col).
        Returns True if the action was legal, False otherwise. The
        internal game state is updated (playing / won / lost).
        """
        if self.state != STATE_PLAYING:
            return False
        cell = self.board[row][col]
        if cell.is_revealed or cell.is_flagged:
            return False
        if not self.mines_placed:
            self.place_mines(row, col)
        if cell.is_mine:
            cell.is_revealed = True
            cell.is_exploded = True  # red highlight in the GUI
            self.state = STATE_LOST
            self._reveal_all_mines()
            return True
        self._flood_fill(row, col)
        if self._check_win():
            self.state = STATE_WON
            self._flag_remaining_mines()
        return True
    def toggle_flag(self, row, col):
        """Flag or unflag the cell at (row, col). Returns True on success."""
        if self.state != STATE_PLAYING:
            return False
        changed = self.board[row][col].toggle_flag()
        if changed:
            self.flags_used += 1 if self.board[row][col].is_flagged else -1
        return changed
    def _flood_fill(self, row, col):
        """Iteratively reveal the cell and, for empty cells, its neighbours."""
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            cell = self.board[r][c]
            if cell.is_revealed or cell.is_flagged or cell.is_mine:
                continue
            cell.is_revealed = True
            self.revealed_count += 1
            if cell.adjacent_mines == 0:
                for nr, nc in self._neighbors(r, c):
                    if not self.board[nr][nc].is_revealed:
                        stack.append((nr, nc))
    def _reveal_all_mines(self):
        """Reveal every mine (used when the player loses)."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c].is_mine:
                    self.board[r][c].is_revealed = True
    def _flag_remaining_mines(self):
        """Auto-flag every mine when the game is won."""
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.board[r][c]
                if cell.is_mine and not cell.is_flagged:
                    cell.is_flagged = True
                    self.flags_used += 1  # keep the mine counter consistent
    def _check_win(self):
        """The game is won when every non-mine cell has been revealed."""
        total_safe = self.rows * self.cols - self.mines
        return self.revealed_count >= total_safe
    # ------------------------------------------------------------------
    # Helpers for the GUI
    # ------------------------------------------------------------------
    def get_cell(self, row, col):
        """Return the Cell object located at (row, col)."""
        return self.board[row][col]
    def remaining_mines(self):
        """Number of mines not yet flagged (can be negative)."""
        return self.mines - self.flags_used