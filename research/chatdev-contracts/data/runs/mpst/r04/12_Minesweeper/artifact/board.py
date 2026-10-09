'''
board.py
Defines the Board class: the complete Minesweeper game logic, including
mine placement (safe first click), flood-fill revealing, flag toggling,
chording, and win/loss detection.
'''
import random
from cell import Cell
class Board:
    """Represents the Minesweeper game board and its logic."""
    def __init__(self, rows, cols, mine_count):
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.mines_placed = False
        self.game_over = False
        self.game_won = False
        self.revealed_safe_cells = 0
    def get_cell(self, row, col):
        """Return the cell at (row, col), or None if out of bounds."""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None
    def get_neighbors(self, row, col):
        """Return the cells adjacent to (row, col) in 8 directions."""
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                cell = self.get_cell(row + dr, col + dc)
                if cell is not None:
                    neighbors.append(cell)
        return neighbors
    def place_mines(self, safe_row, safe_col):
        """Place mines randomly, avoiding the first-clicked cell and its neighbors."""
        forbidden = {(safe_row, safe_col)}
        for n in self.get_neighbors(safe_row, safe_col):
            forbidden.add((n.row, n.col))
        total_cells = self.rows * self.cols
        if len(forbidden) + self.mine_count > total_cells:
            forbidden = {(safe_row, safe_col)}
        available = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) not in forbidden
        ]
        mine_positions = random.sample(available, self.mine_count)
        for r, c in mine_positions:
            self.grid[r][c].is_mine = True
        # Compute adjacent mine counts
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if not cell.is_mine:
                    cell.adjacent_mines = sum(1 for n in self.get_neighbors(r, c) if n.is_mine)
        self.mines_placed = True
    def reveal_cell(self, row, col):
        """Reveal a cell; flood-fill reveals empty regions. Returns list of newly revealed cells."""
        if self.game_over:
            return []
        cell = self.get_cell(row, col)
        if cell is None or cell.is_revealed or cell.is_flagged:
            return []
        if not self.mines_placed:
            self.place_mines(row, col)
        newly_revealed = []
        if cell.is_mine:
            self._reveal_all_mines()
            cell.is_revealed = True
            self.game_over = True
            self.game_won = False
            newly_revealed.append(cell)
            return newly_revealed
        self._flood_fill(cell, newly_revealed)
        self._check_win()
        return newly_revealed
    def _flood_fill(self, start_cell, revealed_list):
        """Iteratively reveal the connected empty region starting at start_cell."""
        stack = [start_cell]
        while stack:
            cell = stack.pop()
            if cell.is_revealed or cell.is_flagged or cell.is_mine:
                continue
            cell.is_revealed = True
            self.revealed_safe_cells += 1
            revealed_list.append(cell)
            if cell.adjacent_mines == 0:
                for n in self.get_neighbors(cell.row, cell.col):
                    if not n.is_revealed and not n.is_flagged and not n.is_mine:
                        stack.append(n)
    def _reveal_all_mines(self):
        """Reveal every mine on the board (used when a mine is uncovered)."""
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.is_mine:
                    cell.is_revealed = True
    def toggle_flag(self, row, col):
        """Place or remove a flag on an unrevealed cell. Returns the cell, or None."""
        if self.game_over:
            return None
        cell = self.get_cell(row, col)
        if cell is None or cell.is_revealed:
            return None
        cell.is_flagged = not cell.is_flagged
        return cell
    def chord(self, row, col):
        """If a revealed numbered cell has the correct number of flags around it, reveal remaining neighbors."""
        cell = self.get_cell(row, col)
        if cell is None or not cell.is_revealed or cell.adjacent_mines == 0:
            return []
        neighbors = self.get_neighbors(row, col)
        flags = sum(1 for n in neighbors if n.is_flagged)
        if flags != cell.adjacent_mines:
            return []
        newly_revealed = []
        for n in neighbors:
            if not n.is_flagged and not n.is_revealed:
                newly_revealed.extend(self.reveal_cell(n.row, n.col))
                if self.game_over:
                    break
        return newly_revealed
    def count_flags(self):
        """Return the total number of flags currently placed."""
        return sum(1 for r in range(self.rows) for c in range(self.cols) if self.grid[r][c].is_flagged)
    def _check_win(self):
        """Win when every safe cell has been revealed; auto-flag remaining mines."""
        total_safe = self.rows * self.cols - self.mine_count
        if self.revealed_safe_cells >= total_safe:
            self.game_won = True
            self.game_over = True
            # Auto-flag remaining mines
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.grid[r][c]
                    if cell.is_mine and not cell.is_flagged:
                        cell.is_flagged = True