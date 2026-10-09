'''
game_logic.py
Core game logic for the 2048 game. This module is completely independent
of any GUI framework and contains the full rules of 2048:
    * 4x4 grid of tiles
    * Sliding tiles in one of four directions with the arrow keys
    * Merging equal tiles (doubling their value, each tile merges once per move)
    * Spawning a new tile (2 with 90% probability, 4 with 10% probability)
      in a random empty cell after every successful move
    * Score tracking (every merge adds the value of the produced tile)
    * Highest-tile tracking
    * Game-over detection (no empty cells and no possible merges)
'''
import random
# Direction constants
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)
class Game2048:
    """Model of the 2048 game: grid state, moves, merges, score and game-over rules."""
    def __init__(self, size=4, seed=None):
        self.size = size
        self.rng = random.Random(seed)
        self.reset()
    def reset(self):
        """Start a fresh game: empty grid, zero score, two random starting tiles."""
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.highest_tile = 0
        self.game_over = False
        self.spawn_tile()
        self.spawn_tile()
    # ------------------------------------------------------------------ #
    # Tile spawning
    # ------------------------------------------------------------------ #
    def empty_cells(self):
        """Return a list of (row, col) tuples for every empty cell."""
        cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    cells.append((r, c))
        return cells
    def spawn_tile(self):
        """Place a new tile (2 with 90% chance, 4 with 10%) in a random empty cell."""
        cells = self.empty_cells()
        if not cells:
            return False
        r, c = self.rng.choice(cells)
        self.grid[r][c] = 2 if self.rng.random() < 0.9 else 4
        self.highest_tile = max(self.highest_tile, self.grid[r][c])
        return True
    # ------------------------------------------------------------------ #
    # Core sliding / merging
    # ------------------------------------------------------------------ #
    @staticmethod
    def _slide_and_merge_line(line):
        """
        Slide and merge one line towards index 0.
        Returns (new_line, gained_score, moved) where:
            new_line     - the resulting line after sliding + merging
            gained_score - points earned by merges on this line
            moved        - True if the line changed at all
        """
        tiles = [v for v in line if v != 0]
        new_line = []
        gained = 0
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                merged = tiles[i] * 2
                new_line.append(merged)
                gained += merged
                i += 2          # each tile may merge only once per move
            else:
                new_line.append(tiles[i])
                i += 1
        new_line += [0] * (len(line) - len(new_line))
        moved = new_line != list(line)
        return new_line, gained, moved
    def _extract_line(self, direction, index):
        """Extract line `index` from the grid oriented so that index 0 is the move target."""
        if direction == LEFT:
            return list(self.grid[index])
        if direction == RIGHT:
            return list(reversed(self.grid[index]))
        if direction == UP:
            return [self.grid[r][index] for r in range(self.size)]
        if direction == DOWN:
            return [self.grid[r][index] for r in reversed(range(self.size))]
        raise ValueError(f'Unknown direction: {direction}')
    def _write_line(self, direction, index, line):
        """Write a processed line back into the grid (inverse of _extract_line)."""
        if direction == LEFT:
            self.grid[index] = list(line)
        elif direction == RIGHT:
            self.grid[index] = list(reversed(line))
        elif direction == UP:
            for r in range(self.size):
                self.grid[r][index] = line[r]
        elif direction == DOWN:
            for r in range(self.size):
                self.grid[self.size - 1 - r][index] = line[r]
        else:
            raise ValueError(f'Unknown direction: {direction}')
    def move(self, direction):
        """
        Perform one move in the given direction.
        Returns True if the board changed (a legal move was made),
        False if nothing moved. On a successful move the score is
        updated and a new tile is spawned.
        """
        if self.game_over:
            return False
        if direction not in DIRECTIONS:
            raise ValueError(f'Unknown direction: {direction}')
        moved = False
        gained_total = 0
        for index in range(self.size):
            line = self._extract_line(direction, index)
            new_line, gained, line_moved = self._slide_and_merge_line(line)
            if line_moved:
                moved = True
                self._write_line(direction, index, new_line)
            gained_total += gained
        if moved:
            self.score += gained_total
            self.spawn_tile()
            self.highest_tile = max(self.highest_tile, self._max_tile_on_grid())
            if not self.can_move():
                self.game_over = True
        return moved
    def _max_tile_on_grid(self):
        return max(max(row) for row in self.grid)
    # ------------------------------------------------------------------ #
    # Game-over detection
    # ------------------------------------------------------------------ #
    def can_move(self):
        """A move is possible if any cell is empty or any two neighbours are equal."""
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
    def is_game_over(self):
        """The game is over when no move is possible anymore."""
        return not self.can_move()
    # ------------------------------------------------------------------ #
    # Info helpers
    # ------------------------------------------------------------------ #
    def get_score(self):
        return self.score
    def get_highest_tile(self):
        return self.highest_tile
    def get_grid(self):
        """Return a copy of the grid so the UI cannot mutate the model."""
        return [row[:] for row in self.grid]