'''
board.py
Defines the Board class, representing the Minesweeper playfield as a 2D
grid of Cell objects. Handles first-click-safe mine placement, neighbor
lookup, flood-fill revealing, flag toggling, chording, and win detection.
'''
import random
from collections import deque
from cell import Cell
class Board:
    """A rectangular grid of Cells with a fixed number of hidden mines."""
    def __init__(self, width, height, mines):
        if width <= 0 or height <= 0:
            raise ValueError("Board dimensions must be positive")
        if mines < 0 or mines >= width * height:
            raise ValueError("Invalid mine count for board size")
        self.width = width
        self.height = height
        self.mine_count = mines
        self.mines_placed = False
        self.grid = [[Cell(r, c) for c in range(width)] for r in range(height)]
    def in_bounds(self, row, col):
        """True when (row, col) lies inside the board."""
        return 0 <= row < self.height and 0 <= col < self.width
    def get_cell(self, row, col):
        """Return the Cell at (row, col), or None when out of bounds."""
        if self.in_bounds(row, col):
            return self.grid[row][col]
        return None
    def get_neighbors(self, row, col):
        """Return the (up to 8) in-bounds neighbors of (row, col)."""
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                neighbor = self.get_cell(row + dr, col + dc)
                if neighbor is not None:
                    neighbors.append(neighbor)
        return neighbors
    def place_mines(self, safe_row, safe_col):
        """Randomly distribute mines, keeping the first-clicked cell and its
        neighbors mine-free so the opening move is always safe."""
        forbidden = {self.get_cell(safe_row, safe_col)}
        forbidden.update(self.get_neighbors(safe_row, safe_col))
        candidates = [cell for row in self.grid for cell in row
                      if cell not in forbidden]
        random.shuffle(candidates)
        for cell in candidates[:self.mine_count]:
            cell.is_mine = True
        for row in self.grid:
            for cell in row:
                if not cell.is_mine:
                    cell.adjacent_mines = sum(
                        1 for n in self.get_neighbors(cell.row, cell.col)
                        if n.is_mine)
        self.mines_placed = True
    def toggle_flag(self, row, col):
        """Toggle a flag on a hidden cell. Returns True if the state changed."""
        cell = self.get_cell(row, col)
        if cell is None:
            return False
        return cell.toggle_flag()
    def reveal(self, row, col):
        """Reveal the cell at (row, col), flood-filling empty regions.
        Returns (hit_mine, revealed_cells)."""
        cell = self.get_cell(row, col)
        if cell is None or cell.is_revealed or cell.is_flagged:
            return False, []
        if not self.mines_placed:
            self.place_mines(row, col)
        cell.reveal()
        revealed = [cell]
        if cell.is_mine:
            return True, revealed
        if cell.adjacent_mines == 0:
            queue = deque([cell])
            while queue:
                current = queue.popleft()
                for neighbor in self.get_neighbors(current.row, current.col):
                    if (not neighbor.is_revealed and not neighbor.is_flagged
                            and not neighbor.is_mine):
                        neighbor.reveal()
                        revealed.append(neighbor)
                        if neighbor.adjacent_mines == 0:
                            queue.append(neighbor)
        return False, revealed
    def chord(self, row, col):
        """Reveal the unrevealed, unflagged neighbors of a revealed cell whose
        adjacent-mine count equals its flagged-neighbor count.
        Returns (hit_mine, revealed_cells)."""
        cell = self.get_cell(row, col)
        if cell is None or not cell.is_revealed or cell.adjacent_mines == 0:
            return False, []
        neighbors = self.get_neighbors(row, col)
        if sum(1 for n in neighbors if n.is_flagged) != cell.adjacent_mines:
            return False, []
        hit_mine = False
        revealed = []
        for neighbor in neighbors:
            if neighbor.is_revealed or neighbor.is_flagged:
                continue
            if neighbor.is_mine:
                neighbor.reveal()
                revealed.append(neighbor)
                hit_mine = True
            else:
                mine_hit, opened = self.reveal(neighbor.row, neighbor.col)
                hit_mine = hit_mine or mine_hit
                revealed.extend(opened)
        return hit_mine, revealed
    def is_cleared(self):
        """True when every non-mine cell has been revealed."""
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True
    def reveal_all_mines(self):
        """Uncover every mine (used when the game is lost)."""
        for row in self.grid:
            for cell in row:
                if cell.is_mine:
                    cell.is_revealed = True