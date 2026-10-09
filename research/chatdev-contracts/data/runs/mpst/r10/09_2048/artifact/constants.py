import random
from constants import GRID_SIZE
class Game:
    """Holds the 2048 board state and implements all game rules."""
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.highest_tile = 0
        self.game_over = False
        self.reset()
    def reset(self):
        """Reset the board, score and highest tile, then spawn two starting tiles."""
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.highest_tile = 0
        self.game_over = False
        self.spawn_tile()
        self.spawn_tile()
        self._update_highest_tile()
    def spawn_tile(self):
        """Place a new tile (90% chance of 2, 10% chance of 4) in a random empty cell."""
        empty_cells = [(r, c) for r in range(GRID_SIZE)
                       for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if not empty_cells:
            return
        row, col = random.choice(empty_cells)
        self.grid[row][col] = 2 if random.random() < 0.9 else 4
        self._update_highest_tile()
    def _update_highest_tile(self):
        """Refresh the highest tile value reached so far."""
        current_max = max(max(row) for row in self.grid)
        if current_max > self.highest_tile:
            self.highest_tile = current_max
    def get_highest_tile(self):
        """Return the highest tile value currently on the board."""
        return max(max(row) for row in self.grid)
    def move(self, direction):
        """
        Slide and merge all tiles in the given direction ('up', 'down', 'left', 'right').
        Returns True if the board changed (a valid move was made), False otherwise.
        """
        if self.game_over:
            return False
        original_grid = [row[:] for row in self.grid]
        gained_score = 0
        if direction == 'left':
            for r in range(GRID_SIZE):
                self.grid[r], gained = self._slide_and_merge_line(self.grid[r])
                gained_score += gained
        elif direction == 'right':
            for r in range(GRID_SIZE):
                reversed_line, gained = self._slide_and_merge_line(self.grid[r][::-1])
                self.grid[r] = reversed_line[::-1]
                gained_score += gained
        elif direction == 'up':
            for c in range(GRID_SIZE):
                column = [self.grid[r][c] for r in range(GRID_SIZE)]
                new_column, gained = self._slide_and_merge_line(column)
                for r in range(GRID_SIZE):
                    self.grid[r][c] = new_column[r]
                gained_score += gained
        elif direction == 'down':
            for c in range(GRID_SIZE):
                column = [self.grid[r][c] for r in range(GRID_SIZE)]
                reversed_column, gained = self._slide_and_merge_line(column[::-1])
                new_column = reversed_column[::-1]
                for r in range(GRID_SIZE):
                    self.grid[r][c] = new_column[r]
                gained_score += gained
        else:
            return False
        gained_score  # unused? no, it's used below
        self.score += gained_score
        if self.grid != original_grid:
            self.spawn_tile()
            self._update_highest_tile()
            if not self.can_move():
                self.game_over = True
            return True
        return False
    @staticmethod
    def _slide_and_merge_line(line):
        """
        Slide a single line toward index 0, merging equal neighbours once each.
        Returns (new_line, score_gained).
        """
        non_zero = [value for value in line if value != 0]
        merged = []
        score_gained = 0
        i = 0
        while i < len(non_zero):
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged_value = non_zero[i] * 2
                merged.append(merged_value)
                score_gained += merged_value
                i += 2
            else:
                merged.append(non_zero[i])
                i += 1
        merged.extend([0] * (len(line) - len(merged)))
        return merged, score_gained
    def can_move(self):
        """Return True if at least one move (slide or merge) is possible."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = self.grid[r][c]
                if value == 0:
                    return True
                if c + 1 < GRID_SIZE and self.grid[r][c + 1] == value:
                    return True
                if r + 1 < GRID_SIZE and self.grid[r + 1][c] == value:
                    return True
        return False
    def is_game_over(self):
        """Return True when no moves are possible anymore."""
        return self.game_over