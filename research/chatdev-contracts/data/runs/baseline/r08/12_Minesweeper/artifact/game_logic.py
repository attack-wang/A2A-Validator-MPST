'''
game_logic.py
Core game logic for Minesweeper.
Contains the Cell and Board classes: mine placement with a safe first
click, adjacency counting, iterative flood-fill revealing, flagging,
and win/lose detection. This module is fully independent of the GUI.
'''
import random
class Cell:
    """Represents a single cell on the Minesweeper board."""
    __slots__ = ("row", "col", "is_mine", "is_revealed", "is_flagged", "adjacent_mines")
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
    def reveal(self):
        """Mark the cell as revealed."""
        self.is_revealed = True
    def toggle_flag(self):
        """Toggle the flag state; only allowed on unrevealed cells. Returns new state."""
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
        return self.is_flagged
    def __repr__(self):
        return (f"Cell({self.row}, {self.col}, mine={self.is_mine}, "
                f"revealed={self.is_revealed}, flagged={self.is_flagged})")
class Board:
    """Game board: mine placement, adjacency counting, reveal flood-fill, win/lose state."""
    def __init__(self, rows, cols, num_mines):
        if num_mines >= rows * cols:
            raise ValueError("Too many mines for board size")
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.mines_placed = False
        self.game_over = False
        self.won = False
        self.cells = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.flags_placed = 0
        self.revealed_count = 0
    def in_bounds(self, row, col):
        """Return True if (row, col) lies inside the board."""
        return 0 <= row < self.rows and 0 <= col < self.cols
    def get_cell(self, row, col):
        """Return the Cell at (row, col), or None if out of bounds."""
        if self.in_bounds(row, col):
            return self.cells[row][col]
        return None
    def get_neighbors(self, row, col):
        """Yield the (up to 8) neighboring cells of (row, col)."""
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                cell = self.get_cell(row + dr, col + dc)
                if cell is not None:
                    yield cell
    def place_mines(self, safe_row, safe_col):
        """Randomly place mines, guaranteeing the first-clicked cell and its neighbors are safe."""
        safe_zone = {(safe_row, safe_col)}
        for cell in self.get_neighbors(safe_row, safe_col):
            safe_zone.add((cell.row, cell.col))
        # If the safe zone is too big relative to the mine count, shrink to just the clicked cell
        available = [(r, c) for r in range(self.rows) for c in range(self.cols)
                     if (r, c) not in safe_zone]
        if len(available) < self.num_mines:
            available = [(r, c) for r in range(self.rows) for c in range(self.cols)
                         if (r, c) != (safe_row, safe_col)]
        mine_positions = random.sample(available, self.num_mines)
        for r, c in mine_positions:
            self.cells[r][c].is_mine = True
        self._calculate_adjacent_mines()
        self.mines_placed = True
    def _calculate_adjacent_mines(self):
        """Compute the adjacent-mine count for every non-mine cell."""
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.cells[r][c]
                if not cell.is_mine:
                    cell.adjacent_mines = sum(1 for n in self.get_neighbors(r, c) if n.is_mine)
    def reveal_cell(self, row, col):
        """
        Reveal the cell at (row, col).
        Returns "mine" if a mine was hit, "ok" otherwise.
        Flood-fills empty regions. Ignores flagged cells during flood fill.
        """
        if self.game_over:
            return "ok"
        cell = self.get_cell(row, col)
        if cell is None or cell.is_revealed or cell.is_flagged:
            return "ok"
        if not self.mines_placed:
            self.place_mines(row, col)
        cell.reveal()
        self.revealed_count += 1
        if cell.is_mine:
            self.game_over = True
            self.won = False
            return "mine"
        if cell.adjacent_mines == 0:
            self._flood_fill(row, col)
        self._check_win()
        return "ok"
    def _flood_fill(self, row, col):
        """Iterative flood fill from (row, col) revealing the connected zero-adjacency region."""
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            for neighbor in self.get_neighbors(r, c):
                if neighbor.is_revealed or neighbor.is_flagged or neighbor.is_mine:
                    continue
                neighbor.reveal()
                self.revealed_count += 1
                if neighbor.adjacent_mines == 0:
                    stack.append((neighbor.row, neighbor.col))
    def toggle_flag(self, row, col):
        """Toggle a flag on a cell; returns True if the cell is now flagged."""
        if self.game_over:
            return False
        cell = self.get_cell(row, col)
        if cell is None or cell.is_revealed:
            return cell.is_flagged if cell else False
        was_flagged = cell.is_flagged
        cell.toggle_flag()
        if cell.is_flagged and not was_flagged:
            self.flags_placed += 1
        elif was_flagged and not cell.is_flagged:
            self.flags_placed -= 1
        return cell.is_flagged
    def _check_win(self):
        """Win when every non-mine cell has been revealed."""
        if self.revealed_count == self.rows * self.cols - self.num_mines:
            self.game_over = True
            self.won = True
            # Auto-flag remaining mines for a tidy final board
            for r in range(self.rows):
                for c in range(self.cols):
                    cell = self.cells[r][c]
                    if cell.is_mine and not cell.is_flagged:
                        cell.is_flagged = True
                        self.flags_placed += 1
    def reveal_all_mines(self):
        """Reveal every unflagged mine (used when the player loses); correct flags stay shown."""
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.cells[r][c]
                if cell.is_mine and not cell.is_flagged:
                    cell.is_revealed = True
    def remaining_mines(self):
        """Number of mines not yet flagged (can go negative if over-flagging)."""
        return self.num_mines - self.flags_placed