'''
Game logic for the Minesweeper board.
The Board class manages the grid of Cells, mine placement (with a
"first click is never a mine" guarantee), flood-fill revealing of empty
regions, flagging, chording, win/lose detection and end-game disclosures.
'''
import random
from cell import Cell
class Board:
    """Logical representation of the Minesweeper playing field."""
    def __init__(self, rows, cols, num_mines):
        """
        Create an empty board.
        Args:
            rows (int): number of rows.
            cols (int): number of columns.
            num_mines (int): number of mines to place once the game starts.
        """
        if num_mines >= rows * cols:
            raise ValueError("Too many mines for the board size.")
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.mines_placed = False
        self.game_over = False
        self.won = False
        self.exploded_cell = None          # (row, col) of the mine hit
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
    # ------------------------------------------------------------------
    # Basic queries
    # ------------------------------------------------------------------
    def in_bounds(self, row, col):
        """Return True if (row, col) lies inside the board."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    def neighbors(self, row, col):
        """Yield the (r, c) coordinates of the up-to-8 neighbours."""
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self.in_bounds(r, c):
                    yield r, c
    def cell(self, row, col):
        """Return the Cell object at (row, col)."""
        return self.grid[row][col]
    def flags_count(self):
        """Number of cells currently flagged."""
        return sum(1 for row in self.grid for c in row if c.is_flagged)
    def revealed_count(self):
        """Number of cells currently revealed."""
        return sum(1 for row in self.grid for c in row if c.is_revealed)
    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def place_mines(self, safe_row, safe_col):
        """
        Randomly distribute the mines, guaranteeing that the first clicked
        cell (and, when space allows, its neighbours) is mine-free.
        """
        forbidden = {(safe_row, safe_col)}
        forbidden.update(self.neighbors(safe_row, safe_col))
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        if len(all_cells) - len(forbidden) < self.num_mines:
            # Extremely small boards: only protect the clicked cell itself.
            forbidden = {(safe_row, safe_col)}
        candidates = [pos for pos in all_cells if pos not in forbidden]
        mines = random.sample(candidates, self.num_mines)
        for r, c in mines:
            self.grid[r][c].is_mine = True
        self._calculate_adjacent_mines()
        self.mines_placed = True
    def _calculate_adjacent_mines(self):
        """Compute the adjacent-mine counter of every cell."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c].adjacent_mines = sum(
                    1 for nr, nc in self.neighbors(r, c) if self.grid[nr][nc].is_mine
                )
    # ------------------------------------------------------------------
    # Player actions
    # ------------------------------------------------------------------
    def reveal_cell(self, row, col):
        """
        Reveal the cell at (row, col).
        Returns a list of (row, col) tuples that were newly revealed
        (empty when the click had no effect, e.g. on a flagged cell).
        Sets self.game_over / self.exploded_cell when a mine is hit.
        """
        if self.game_over:
            return []
        if not self.mines_placed:
            self.place_mines(row, col)
        cell = self.grid[row][col]
        if cell.is_flagged or cell.is_revealed:
            return []
        if cell.is_mine:
            cell.reveal()
            self.exploded_cell = (row, col)
            self.game_over = True
            self.won = False
            return [(row, col)]
        revealed = []
        self._flood_reveal(row, col, revealed)
        if self.check_win():
            self.game_over = True
            self.won = True
        return revealed
    def _flood_reveal(self, row, col, revealed):
        """Iterative flood fill: reveal the cell and, for empty cells,
        every reachable neighbour."""
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            cell = self.grid[r][c]
            if cell.is_revealed or cell.is_flagged or cell.is_mine:
                continue
            cell.reveal()
            revealed.append((r, c))
            if cell.adjacent_mines == 0:
                for nr, nc in self.neighbors(r, c):
                    if not self.grid[nr][nc].is_revealed:
                        stack.append((nr, nc))
    def toggle_flag(self, row, col):
        """Flag / unflag the cell at (row, col). Returns True on change."""
        if self.game_over:
            return False
        return self.grid[row][col].toggle_flag()
    def chord(self, row, col):
        """
        Middle-click convenience: clicking an already-revealed number whose
        adjacent flag count matches reveals its remaining hidden neighbours.
        Returns a list of (row, col) tuples newly revealed.
        """
        cell = self.grid[row][col]
        if self.game_over or not cell.is_revealed or cell.is_mine:
            return []
        flagged = sum(1 for r, c in self.neighbors(row, col)
                      if self.grid[r][c].is_flagged)
        if flagged != cell.adjacent_mines:
            return []
        revealed = []
        for r, c in self.neighbors(row, col):
            n = self.grid[r][c]
            if not n.is_flagged and not n.is_revealed:
                revealed.extend(self.reveal_cell(r, c))
                if self.game_over:
                    # A mine exploded while chording: stop immediately.
                    break
        return revealed
    # ------------------------------------------------------------------
    # End-game helpers
    # ------------------------------------------------------------------
    def check_win(self):
        """The game is won when every non-mine cell is revealed."""
        total_safe = self.rows * self.cols - self.num_mines
        return self.revealed_count() >= total_safe
    def reveal_all_mines(self):
        """Reveal every mine (used when the game is lost)."""
        for row in self.grid:
            for cell in row:
                if cell.is_mine:
                    cell.is_revealed = True