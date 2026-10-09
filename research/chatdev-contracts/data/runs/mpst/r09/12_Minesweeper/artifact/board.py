"""
Game-board logic for the Minesweeper game.
The Board class owns the grid of Cells and implements all rules of the
game: random mine placement (with a safe first click), adjacency counting,
flood-fill revealing of empty regions, flagging, chording, and win/lose
detection.
"""
import random
from cell import Cell
STATUS_READY = "ready"
STATUS_PLAYING = "playing"
STATUS_WON = "won"
STATUS_LOST = "lost"
class Board:
    """Holds the grid of cells and enforces the rules of Minesweeper."""
    def __init__(self, rows, cols, num_mines):
        if num_mines >= rows * cols:
            raise ValueError(
                "Number of mines ({}) must be smaller than the number of "
                "cells ({}x{}={}).".format(num_mines, rows, cols, rows * cols)
            )
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.status = STATUS_READY
        self.cells = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.explosion_site = None  # (row, col) of the mine that was revealed
    def reset(self):
        """Restore every cell and all game state to the initial state."""
        for row in self.cells:
            for cell in row:
                cell.reset()
        self.status = STATUS_READY
        self.explosion_site = None
    def in_bounds(self, row, col):
        """Return True if (row, col) lies inside the board."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    def neighbors(self, row, col):
        """Return the list of cells adjacent to (row, col) (8-neighborhood)."""
        result = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self.in_bounds(r, c):
                    result.append(self.cells[r][c])
        return result
    def place_mines(self, safe_row, safe_col):
        """Randomly place mines, keeping the first-clicked cell and its
        neighbors mine-free so the opening move is never a loss."""
        safe_zone = {self.cells[safe_row][safe_col]}
        safe_zone.update(self.neighbors(safe_row, safe_col))
        candidates = [cell for row in self.cells for cell in row
                      if cell not in safe_zone]
        # If the safe zone is too large (tiny boards), fall back to
        # excluding only the clicked cell.
        if len(candidates) < self.num_mines:
            candidates = [cell for row in self.cells for cell in row
                          if cell is not self.cells[safe_row][safe_col]]
        mines = random.sample(candidates, self.num_mines)
        for cell in mines:
            cell.is_mine = True
        self._compute_adjacent_counts()
        self.status = STATUS_PLAYING
    def _compute_adjacent_counts(self):
        """Compute, for every non-mine cell, how many neighboring cells
        contain mines."""
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.cells[r][c]
                if cell.is_mine:
                    cell.adjacent_mines = 0
                else:
                    cell.adjacent_mines = sum(
                        1 for n in self.neighbors(r, c) if n.is_mine)
    def reveal(self, row, col):
        """Reveal the cell at (row, col).
        Returns True if the move was applied, False if it was ignored
        (game over, flagged cell, or already revealed).
        """
        if self.status not in (STATUS_READY, STATUS_PLAYING):
            return False
        if not self.in_bounds(row, col):
            return False
        cell = self.cells[row][col]
        if not cell.can_reveal():
            return False
        if self.status == STATUS_READY:
            self.place_mines(row, col)
        if cell.is_mine:
            self._lose(cell)
            return True
        self._flood_fill(row, col)
        if self.is_won():
            self.status = STATUS_WON
        return True
    def _flood_fill(self, row, col):
        """Iteratively reveal the cell and, for empty (zero-adjacent) cells,
        cascade to all of their neighbors."""
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            cell = self.cells[r][c]
            if cell.is_revealed or cell.is_flagged or cell.is_mine:
                continue
            cell.is_revealed = True
            if cell.adjacent_mines == 0:
                for n in self.neighbors(r, c):
                    if not n.is_revealed and not n.is_flagged and not n.is_mine:
                        stack.append((n.row, n.col))
    def toggle_flag(self, row, col):
        """Toggle a flag on the cell at (row, col).
        Returns True if the state changed, False if the move was ignored
        (game over or already revealed cell).
        """
        if self.status not in (STATUS_READY, STATUS_PLAYING):
            return False
        if not self.in_bounds(row, col):
            return False
        return self.cells[row][col].toggle_flag()
    def chord(self, row, col):
        """Chording: left-clicking a revealed number whose adjacent flags
        match its count reveals all remaining hidden, unflagged neighbors."""
        if self.status != STATUS_PLAYING:
            return False
        if not self.in_bounds(row, col):
            return False
        cell = self.cells[row][col]
        if not cell.is_revealed or cell.adjacent_mines == 0:
            return False
        nbrs = self.neighbors(row, col)
        flags = sum(1 for n in nbrs if n.is_flagged)
        if flags != cell.adjacent_mines:
            return False
        applied = False
        for n in nbrs:
            if not n.is_revealed and not n.is_flagged:
                if n.is_mine:
                    self._lose(n)
                    return True
                self._flood_fill(n.row, n.col)
                applied = True
                if self.status == STATUS_LOST:
                    return True
        if self.is_won():
            self.status = STATUS_WON
        return applied
    def is_won(self):
        """The game is won when every non-mine cell has been revealed."""
        for row in self.cells:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True
    def _lose(self, cell):
        """Handle the loss: record the explosion site and update status."""
        cell.is_revealed = True
        self.explosion_site = (cell.row, cell.col)
        self.status = STATUS_LOST
    def flags_placed(self):
        """Return the number of flags currently on the board."""
        return sum(1 for row in self.cells for cell in row if cell.is_flagged)