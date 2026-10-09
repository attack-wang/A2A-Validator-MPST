'''
game_logic.py
Core 2048 engine: grid state, slide/merge logic, random tile spawning,
score tracking, and game-over detection. Contains no GUI dependencies.
'''
import random
class Game2048:
    """Pure-Python model of the 2048 game (4x4 by default)."""
    VALID_DIRECTIONS = ('up', 'down', 'left', 'right')
    def __init__(self, size=4):
        """Create an empty board and start a fresh game."""
        self.size = size
        self.reset()
    def reset(self):
        """Clear the board, zero the score, and spawn two starting tiles."""
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.game_over = False
        self.last_spawn = None
        self.spawn_tile()
        self.spawn_tile()
    # ---------- Public API used by the GUI ----------
    def get_grid(self):
        """Return a defensive copy of the board."""
        return [row[:] for row in self.grid]
    def get_score(self):
        """Return the current score."""
        return self.score
    def get_highest_tile(self):
        """Return the largest tile value currently on the board."""
        return max(max(row) for row in self.grid)
    def is_game_over(self):
        """Return True when no moves are possible."""
        return self.game_over
    def get_last_spawn(self):
        """Return the (row, col) of the most recently spawned tile, or None."""
        return self.last_spawn
    # ---------- Core move handling ----------
    def move(self, direction):
        """Slide all tiles in `direction`; merge equal neighbours once each."""
        if self.game_over or direction not in self.VALID_DIRECTIONS:
            return False
        changed = False
        gained_total = 0
        for index in range(self.size):
            line = self._extract_line(direction, index)
            new_line, gained = self._slide_row_left(line)
            gained_total += gained
            if new_line != line:
                changed = True
            self._write_line(direction, index, new_line)
        if changed:
            self.score += gained_total
            self.spawn_tile()
            if not self._can_move():
                self.game_over = True
        return changed
    def _slide_row_left(self, line):
        """Compress one line left, merging equal neighbours once per move.
        Returns (new_line, points_gained). E.g. [2, 2, 2, 2] -> [4, 4, 0, 0].
        """
        tiles = [v for v in line if v != 0]
        new_line, gained, i = [], 0, 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                merged = tiles[i] * 2
                new_line.append(merged)
                gained += merged
                i += 2  # each tile merges at most once per move
            else:
                new_line.append(tiles[i])
                i += 1
        new_line += [0] * (self.size - len(new_line))
        return new_line, gained
    def _extract_line(self, direction, index):
        """Extract the line (row/column) that slides toward the board edge."""
        if direction == 'left':
            return self.grid[index][:]
        if direction == 'right':
            return self.grid[index][::-1]
        if direction == 'up':
            return [self.grid[r][index] for r in range(self.size)]
        return [self.grid[r][index] for r in range(self.size)][::-1]  # down
    def _write_line(self, direction, index, line):
        """Write a processed line back into the grid."""
        if direction == 'left':
            self.grid[index] = line[:]
        elif direction == 'right':
            self.grid[index] = line[::-1]
        elif direction == 'up':
            for r in range(self.size):
                self.grid[r][index] = line[r]
        else:  # down
            for r in range(self.size):
                self.grid[r][index] = line[self.size - 1 - r]
    # ---------- Spawning and game-over detection ----------
    def spawn_tile(self):
        """Place a 2 (90%) or 4 (10%) in a random empty cell."""
        empty = [(r, c) for r in range(self.size)
                 for c in range(self.size) if self.grid[r][c] == 0]
        if not empty:
            return
        row, col = random.choice(empty)
        self.grid[row][col] = 2 if random.random() < 0.9 else 4
        self.last_spawn = (row, col)
    def _can_move(self):
        """Return True if any slide would change the board."""
        for r in range(self.size):
            for c in range(self.size):
                value = self.grid[r][c]
                if value == 0:
                    return True
                if c + 1 < self.size and self.grid[r][c + 1] == value:
                    return True
                if r + 1 < self.size and self.grid[r + 1][c] == value:
                    return True
        return False