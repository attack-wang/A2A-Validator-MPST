'''
game_logic.py
Core game logic for 2048: grid state, tile movement/merging, spawning, and game-over detection.
'''
import random
from constants import GRID_SIZE
class Game2048:
    """Represents the state and rules of a 2048 game on a GRID_SIZE x GRID_SIZE board."""
    def __init__(self):
        self.reset()
    def reset(self):
        """Reset the board, score, and highest tile; spawn two starting tiles."""
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.highest_tile = 0
        self.game_over = False
        self._spawn_tile()
        self._spawn_tile()
        # FIX: update highest tile immediately so "BEST TILE" is correct at game start
        self._update_highest_tile()
    def _empty_cells(self):
        """Return a list of (row, col) tuples for all empty cells."""
        cells = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == 0:
                    cells.append((r, c))
        return cells
    def _spawn_tile(self):
        """Place a new tile (2 with 90% chance, 4 with 10%) in a random empty cell."""
        empty = self._empty_cells()
        if not empty:
            return
        r, c = random.choice(empty)
        self.grid[r][c] = 2 if random.random() < 0.9 else 4
    def _slide_row_left(self, row):
        """
        Slide and merge one row toward the left.
        Returns (new_row, gained_score).
        """
        # 1. Remove zeros (compress)
        tiles = [v for v in row if v != 0]
        new_row = []
        gained = 0
        i = 0
        while i < len(tiles):
            # 2. Merge equal adjacent tiles once per move
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                merged = tiles[i] * 2
                new_row.append(merged)
                gained += merged
                i += 2
            else:
                new_row.append(tiles[i])
                i += 1
        # 3. Pad with zeros on the right
        new_row.extend([0] * (GRID_SIZE - len(new_row)))
        return new_row, gained
    def move(self, direction):
        """
        Perform a move in the given direction ('left', 'right', 'up', 'down').
        Returns True if the board changed (a valid move was made).
        """
        original = [row[:] for row in self.grid]
        moved = False
        if direction == 'left':
            for r in range(GRID_SIZE):
                self.grid[r], gained = self._slide_row_left(self.grid[r])
                self.score += gained
        elif direction == 'right':
            for r in range(GRID_SIZE):
                reversed_row = self.grid[r][::-1]
                new_row, gained = self._slide_row_left(reversed_row)
                self.grid[r] = new_row[::-1]
                self.score += gained
        elif direction == 'up':
            for c in range(GRID_SIZE):
                column = [self.grid[r][c] for r in range(GRID_SIZE)]
                new_col, gained = self._slide_row_left(column)
                for r in range(GRID_SIZE):
                    self.grid[r][c] = new_col[r]
                self.score += gained
        elif direction == 'down':
            for c in range(GRID_SIZE):
                column = [self.grid[r][c] for r in range(GRID_SIZE)][::-1]
                new_col, gained = self._slide_row_left(column)
                new_col = new_col[::-1]
                for r in range(GRID_SIZE):
                    self.grid[r][c] = new_col[r]
                self.score += gained
        else:
            return False
        moved = self.grid != original
        if moved:
            self._spawn_tile()
            self._update_highest_tile()
            if not self.can_move():
                self.game_over = True
        return moved
    def _update_highest_tile(self):
        """Update the highest tile value seen on the board."""
        for row in self.grid:
            for value in row:
                if value > self.highest_tile:
                    self.highest_tile = value
    def can_move(self):
        """Return True if at least one move (slide or merge) is possible."""
        # If any cell is empty, a move is possible
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == 0:
                    return True
        # Check horizontal merges
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - 1):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return True
        # Check vertical merges
        for c in range(GRID_SIZE):
            for r in range(GRID_SIZE - 1):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False