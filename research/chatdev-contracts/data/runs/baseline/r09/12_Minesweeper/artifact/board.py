'''
board.py
Core game-logic module for the Minesweeper game.
Contains:
    Cell  -- data object holding the state of a single board cell.
    Board -- grid of cells implementing mine placement, adjacency
             counting, revealing (with flood fill), flagging,
             chord revealing and win/lose detection.
'''
import random
from collections import deque
class Cell:
    '''Holds the state of a single Minesweeper cell.'''
    __slots__ = ("is_mine", "is_revealed", "is_flagged", "adjacent_mines")
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
class Board:
    '''Minesweeper board: grid of cells plus all game rules.'''
    def __init__(self, width, height, num_mines):
        if width < 2 or height < 2:
            raise ValueError("Board must be at least 2x2.")
        if num_mines < 1:
            raise ValueError("A board needs at least one mine.")
        if num_mines > width * height - 1:
            raise ValueError("Too many mines for this board size.")
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.cells = [[Cell() for _ in range(width)] for _ in range(height)]
        # Mines are only placed after the first reveal so that the first
        # click is always safe.
        self.mines_placed = False
        self.game_over = False
        self.won = False
        self.exploded_cell = None  # (row, col) of the mine that was hit
    # ------------------------------------------------------------------
    # Geometry helpers
    # ------------------------------------------------------------------
    def in_bounds(self, row, col):
        '''Return True if (row, col) lies inside the board.'''
        return 0 <= row < self.height and 0 <= col < self.width
    def neighbors(self, row, col):
        '''Yield the (row, col) coordinates of the 8 adjacent cells.'''
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if self.in_bounds(nr, nc):
                    yield nr, nc
    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def place_mines(self, safe_row, safe_col):
        '''Randomly place mines, keeping the first-clicked cell (and,
        when possible, its neighborhood) free of mines.'''
        excluded = {(safe_row, safe_col)}
        excluded.update(self.neighbors(safe_row, safe_col))
        available = [(r, c)
                     for r in range(self.height)
                     for c in range(self.width)
                     if (r, c) not in excluded]
        # Very small boards might not be able to honor the full
        # exclusion zone; fall back to protecting only the clicked cell.
        if len(available) < self.num_mines:
            available = [(r, c)
                         for r in range(self.height)
                         for c in range(self.width)
                         if (r, c) != (safe_row, safe_col)]
        for row, col in random.sample(available, self.num_mines):
            self.cells[row][col].is_mine = True
        self._calculate_adjacent_mines()
        self.mines_placed = True
    def _calculate_adjacent_mines(self):
        '''Compute the adjacent-mine count for every non-mine cell.'''
        for r in range(self.height):
            for c in range(self.width):
                cell = self.cells[r][c]
                if not cell.is_mine:
                    cell.adjacent_mines = sum(
                        1 for nr, nc in self.neighbors(r, c)
                        if self.cells[nr][nc].is_mine
                    )
    # ------------------------------------------------------------------
    # Player actions
    # ------------------------------------------------------------------
    def reveal_cell(self, row, col):
        '''Reveal the cell at (row, col).
        Returns True if a mine was uncovered (the player loses), False
        otherwise.  Empty cells flood-fill their neighborhood.
        '''
        if self.game_over:
            return False
        if not self.in_bounds(row, col):
            return False
        cell = self.cells[row][col]
        if cell.is_revealed or cell.is_flagged:
            return False
        if not self.mines_placed:
            self.place_mines(row, col)
        if cell.is_mine:
            cell.is_revealed = True
            self.exploded_cell = (row, col)
            self._lose()
            return True
        self._flood_reveal(row, col)
        self._check_win()
        return False
    def toggle_flag(self, row, col):
        '''Flag / unflag a covered cell.  Ignored after game over,
        on revealed cells or on out-of-bounds coordinates.'''
        if self.game_over or not self.in_bounds(row, col):
            return
        cell = self.cells[row][col]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged
    def chord_reveal(self, row, col):
        '''Classic "chording": left-clicking an already revealed numbered
        cell whose adjacent flag count matches its number reveals every
        other adjacent cell.
        Returns True if a mine was hit while chording.'''
        if self.game_over or not self.in_bounds(row, col):
            return False
        cell = self.cells[row][col]
        if not cell.is_revealed or cell.adjacent_mines == 0:
            return False
        flagged = sum(1 for nr, nc in self.neighbors(row, col)
                      if self.cells[nr][nc].is_flagged)
        if flagged != cell.adjacent_mines:
            return False
        hit_mine = False
        for nr, nc in list(self.neighbors(row, col)):
            neighbor = self.cells[nr][nc]
            if not neighbor.is_revealed and not neighbor.is_flagged:
                if self.reveal_cell(nr, nc):
                    hit_mine = True
                if self.game_over:
                    break
        return hit_mine
    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _flood_reveal(self, row, col):
        '''Iterative flood fill: reveal (row, col) and, for empty cells,
        keep revealing their neighbors.'''
        queue = deque([(row, col)])
        while queue:
            r, c = queue.popleft()
            cell = self.cells[r][c]
            if cell.is_revealed or cell.is_flagged or cell.is_mine:
                continue
            cell.is_revealed = True
            if cell.adjacent_mines == 0:
                for nr, nc in self.neighbors(r, c):
                    neighbor = self.cells[nr][nc]
                    if not neighbor.is_revealed:
                        queue.append((nr, nc))
    def _check_win(self):
        '''The game is won when every non-mine cell is revealed.'''
        if self.game_over:
            return
        for r in range(self.height):
            for c in range(self.width):
                cell = self.cells[r][c]
                if not cell.is_mine and not cell.is_revealed:
                    return
        self.game_over = True
        self.won = True
    def _lose(self):
        '''Handle losing: reveal every mine and mark the game over.'''
        self.game_over = True
        self.won = False
        for r in range(self.height):
            for c in range(self.width):
                if self.cells[r][c].is_mine:
                    self.cells[r][c].is_revealed = True
    # ------------------------------------------------------------------
    # Query helpers used by the GUI
    # ------------------------------------------------------------------
    def flagged_count(self):
        '''Number of currently flagged cells.'''
        return sum(1 for row in self.cells for cell in row if cell.is_flagged)
    def remaining_mines(self):
        '''Mines left to find (total mines minus flags placed).'''
        return self.num_mines - self.flagged_count()
    def revealed_count(self):
        '''Number of revealed cells (used for statistics).'''
        return sum(1 for row in self.cells for cell in row if cell.is_revealed)