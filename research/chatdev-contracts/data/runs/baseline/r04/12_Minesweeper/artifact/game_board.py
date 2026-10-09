'''
game_board.py
Core game logic for the Minesweeper application.
Contains:
- Cell: represents a single cell of the board (mine, revealed, flagged state,
  adjacent mine count).
- Board: represents the full minesweeper board, handles mine placement,
  neighbour counting, flood-fill revealing, flagging and win/lose checks.
'''
import random
class Cell:
    """Represents a single cell on the Minesweeper board."""
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
    def reveal(self):
        """Mark the cell as revealed. Returns True if the state changed."""
        if not self.is_revealed and not self.is_flagged:
            self.is_revealed = True
            return True
        return False
    def toggle_flag(self):
        """Flag / unflag the cell. Only allowed on unrevealed cells."""
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
            return True
        return False
class Board:
    """Represents the Minesweeper board and implements the game rules."""
    def __init__(self, rows, cols, num_mines):
        if num_mines >= rows * cols:
            raise ValueError("Too many mines for the board size.")
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.mines_placed = False
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.won = False
    def in_bounds(self, row, col):
        """Return True if (row, col) lies inside the board."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    def get_cell(self, row, col):
        """Return the Cell at (row, col), or None if out of bounds."""
        if self.in_bounds(row, col):
            return self.grid[row][col]
        return None
    def neighbours(self, row, col):
        """Yield (r, c) coordinates of the 8 neighbours around a cell."""
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self.in_bounds(r, c):
                    yield r, c
    def place_mines(self, safe_row, safe_col):
        """Randomly place mines, keeping the first clicked cell (and its
        neighbours) mine-free so the game always starts with a useful move."""
        safe_zone = {(safe_row, safe_col)}
        safe_zone.update(self.neighbours(safe_row, safe_col))
        # If the safe zone is too large, shrink it to just the clicked cell.
        if len(safe_zone) > self.rows * self.cols - self.num_mines:
            safe_zone = {(safe_row, safe_col)}
        candidates = [(r, c) for r in range(self.rows) for c in range(self.cols)
                      if (r, c) not in safe_zone]
        mines = random.sample(candidates, self.num_mines)
        for r, c in mines:
            self.grid[r][c].is_mine = True
        self._calculate_adjacent_mines()
        self.mines_placed = True
    def _calculate_adjacent_mines(self):
        """Compute the adjacent-mine hint number for every non-mine cell."""
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.grid[r][c].is_mine:
                    count = sum(1 for nr, nc in self.neighbours(r, c)
                                if self.grid[nr][nc].is_mine)
                    self.grid[r][c].adjacent_mines = count
    def reveal_cell(self, row, col):
        """Reveal a cell. Returns 'mine', 'revealed' or 'ignored'."""
        if self.game_over:
            return 'ignored'
        cell = self.get_cell(row, col)
        if cell is None or cell.is_revealed or cell.is_flagged:
            return 'ignored'
        if not self.mines_placed:
            self.place_mines(row, col)
        if cell.is_mine:
            cell.is_revealed = True
            self.game_over = True
            self.won = False
            return 'mine'
        self._flood_fill(row, col)
        if self.check_win():
            self.game_over = True
            self.won = True
        return 'revealed'
    def _flood_fill(self, row, col):
        """Iterative flood fill: reveal the cell and, when it has no adjacent
        mines, keep revealing its neighbours (depth-first, iterative)."""
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            cell = self.get_cell(r, c)
            if cell is None or cell.is_revealed or cell.is_mine or cell.is_flagged:
                continue
            cell.is_revealed = True
            if cell.adjacent_mines == 0:
                for nr, nc in self.neighbours(r, c):
                    ncell = self.get_cell(nr, nc)
                    if ncell and not ncell.is_revealed and not ncell.is_flagged:
                        stack.append((nr, nc))
    def chord(self, row, col):
        """Middle-click style move: if the number of flags around a revealed
        numbered cell matches its value, reveal all other neighbours.
        Returns 'mine' if a mine gets revealed, otherwise 'revealed'/'ignored'."""
        if self.game_over:
            return 'ignored'
        cell = self.get_cell(row, col)
        if cell is None or not cell.is_revealed or cell.adjacent_mines == 0:
            return 'ignored'
        flagged = sum(1 for nr, nc in self.neighbours(row, col)
                      if self.grid[nr][nc].is_flagged)
        if flagged != cell.adjacent_mines:
            return 'ignored'
        result = 'revealed'
        for nr, nc in self.neighbours(row, col):
            ncell = self.grid[nr][nc]
            if not ncell.is_flagged and not ncell.is_revealed:
                outcome = self.reveal_cell(nr, nc)
                if outcome == 'mine':
                    result = 'mine'
        return result
    def toggle_flag(self, row, col):
        """Toggle a flag on a hidden cell. Returns True if the state changed."""
        if self.game_over:
            return False
        cell = self.get_cell(row, col)
        if cell is None:
            return False
        return cell.toggle_flag()
    def count_flags(self):
        """Return the total number of flags currently placed."""
        return sum(1 for r in range(self.rows) for c in range(self.cols)
                   if self.grid[r][c].is_flagged)
    def check_win(self):
        """The game is won when every non-mine cell has been revealed."""
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if not cell.is_mine and not cell.is_revealed:
                    return False
        self.won = True
        return True
    def reveal_all_mines(self):
        """Used when the game ends: reveal every mine."""
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.is_mine:
                    cell.is_revealed = True