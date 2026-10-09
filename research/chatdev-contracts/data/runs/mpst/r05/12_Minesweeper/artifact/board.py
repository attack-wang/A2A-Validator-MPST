'''
board.py
Defines the Board class, which owns the grid of Cells and implements the
core Minesweeper rules:
    * randomised mine placement that guarantees a safe first click,
    * computation of adjacent-mine counters,
    * flood-fill uncovering of empty regions,
    * flag toggling,
    * win / lose detection.
'''
import random
from cell import Cell
class Board:
    """The Minesweeper playing field: a rows x cols grid of Cells."""
    def __init__(self, rows, cols, num_mines):
        """
        Build an empty board.
        Mines are NOT placed here; they are laid out on the player's first
        reveal so that the opening click can never lose the game.
        """
        if rows < 1 or cols < 1:
            raise ValueError("Board dimensions must be positive.")
        if not 0 < num_mines < rows * cols:
            raise ValueError("Mine count must be between 1 and (rows*cols - 1).")
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.cells = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.mines_placed = False   # becomes True after the first reveal
        self.game_over = False
        self.won = False
        self.exploded_cell = None   # the mine that ended a lost game
    # ------------------------------------------------------------------
    # Basic access helpers
    # ------------------------------------------------------------------
    def reset(self):
        """Clear the board so a fresh game can start on the same grid size."""
        for row_cells in self.cells:
            for cell in row_cells:
                cell.reset()
        self.mines_placed = False
        self.game_over = False
        self.won = False
        self.exploded_cell = None
    def in_bounds(self, row, col):
        """True if (row, col) lies inside the board."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    def get_cell(self, row, col):
        """Return the Cell at (row, col)."""
        return self.cells[row][col]
    def all_cells(self):
        """Iterate over every cell on the board."""
        for row_cells in self.cells:
            for cell in row_cells:
                yield cell
    def get_neighbors(self, row, col):
        """Return the (up to eight) cells adjacent to (row, col)."""
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self.in_bounds(r, c):
                    neighbors.append(self.cells[r][c])
        return neighbors
    # ------------------------------------------------------------------
    # Mine placement
    # ------------------------------------------------------------------
    def place_mines(self, safe_row, safe_col):
        """
        Randomly distribute the mines across the board.
        The first-clicked cell (and, when space allows, its neighbours) are
        kept mine-free so the opening move never detonates anything.
        """
        clicked = self.get_cell(safe_row, safe_col)
        safe_zone = {clicked}
        safe_zone.update(self.get_neighbors(safe_row, safe_col))
        candidates = [cell for cell in self.all_cells() if cell not in safe_zone]
        if len(candidates) < self.num_mines:
            # Very dense board: only protect the clicked cell itself.
            candidates = [cell for cell in self.all_cells() if cell is not clicked]
        for mine in random.sample(candidates, self.num_mines):
            mine.is_mine = True
        self.mines_placed = True
        self._calculate_adjacent_mines()
    def _calculate_adjacent_mines(self):
        """Fill in the adjacent-mine counters for every non-mine cell."""
        for cell in self.all_cells():
            if not cell.is_mine:
                cell.adjacent_mines = sum(
                    1 for n in self.get_neighbors(cell.row, cell.col) if n.is_mine
                )
    # ------------------------------------------------------------------
    # Player actions
    # ------------------------------------------------------------------
    def reveal_cell(self, row, col):
        """
        Uncover the cell at (row, col).
        Returns True if the reveal hit a mine (game lost), otherwise False.
        Empty cells trigger a flood fill that uncovers the whole region.
        """
        if self.game_over:
            return False
        cell = self.get_cell(row, col)
        if cell.is_flagged or cell.is_revealed:
            return False
        if not self.mines_placed:
            self.place_mines(row, col)
        if cell.is_mine:
            cell.reveal()
            self.exploded_cell = cell
            self.game_over = True
            self.won = False
            self._reveal_all_mines()
            return True
        self._flood_fill_reveal(cell)
        if self._all_safe_cells_revealed():
            self.game_over = True
            self.won = True
            self._flag_remaining_mines()
        return False
    def toggle_flag(self, row, col):
        """Plant or remove a flag on a covered cell (ignored after game over)."""
        if self.game_over:
            return
        cell = self.get_cell(row, col)
        if not cell.is_revealed:
            cell.toggle_flag()
    def count_flags(self):
        """Number of flags currently planted on the board."""
        return sum(1 for cell in self.all_cells() if cell.is_flagged)
    # ------------------------------------------------------------------
    # Internal rule helpers
    # ------------------------------------------------------------------
    def _flood_fill_reveal(self, start_cell):
        """Iteratively uncover `start_cell` and, for empty cells, their region."""
        stack = [start_cell]
        while stack:
            cell = stack.pop()
            if cell.is_mine or cell.is_revealed or cell.is_flagged:
                continue
            cell.reveal()
            if cell.adjacent_mines == 0:
                for neighbor in self.get_neighbors(cell.row, cell.col):
                    if neighbor.is_hidden:
                        stack.append(neighbor)
    def _all_safe_cells_revealed(self):
        """Win condition: every cell without a mine has been uncovered."""
        return all(cell.is_mine or cell.is_revealed for cell in self.all_cells())
    def _reveal_all_mines(self):
        """After a loss, uncover every mine that was not already flagged."""
        for cell in self.all_cells():
            if cell.is_mine and not cell.is_flagged:
                cell.reveal()
    def _flag_remaining_mines(self):
        """After a win, mark every mine with a flag (classic behaviour)."""
        for cell in self.all_cells():
            if cell.is_mine and not cell.is_flagged:
                cell.state = "flagged"