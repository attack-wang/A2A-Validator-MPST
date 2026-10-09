'''
Core game logic for 2048: grid state, tile spawning, movement/merging,
score tracking, and game-over detection.
'''
import random
from config import GRID_SIZE, SPAWN_PROBABILITY_FOUR, TARGET_TILE
class Game:
    '''Holds the 4x4 board and implements all 2048 rules.'''
    def __init__(self, size=GRID_SIZE):
        self.size = size
        self.reset()
    def reset(self):
        '''Start a fresh game: empty board, zero score, two starter tiles.'''
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.spawn_tile()
        self.spawn_tile()
    # ------------------------------------------------------------------
    # Tile spawning
    # ------------------------------------------------------------------
    def empty_cells(self):
        '''Return a list of (row, col) tuples for all empty cells.'''
        cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    cells.append((r, c))
        return cells
    def spawn_tile(self):
        '''Place a 2 (90%) or 4 (10%) in a random empty cell.'''
        cells = self.empty_cells()
        if not cells:
            return False
        r, c = random.choice(cells)
        value = 4 if random.random() < SPAWN_PROBABILITY_FOUR else 2
        self.grid[r][c] = value
        return True
    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    @staticmethod
    def _slide_row_left(row):
        '''Slide one row to the left, merging equal neighbours once.
        Returns (new_row, score_gained, moved).
        '''
        tiles = [v for v in row if v != 0]
        new_row = []
        score_gained = 0
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                merged = tiles[i] * 2
                new_row.append(merged)
                score_gained += merged
                i += 2
            else:
                new_row.append(tiles[i])
                i += 1
        new_row.extend([0] * (len(row) - len(new_row)))
        moved = new_row != row
        return new_row, score_gained, moved
    def move(self, direction):
        '''Slide all tiles in `direction` ('up'/'down'/'left'/'right').
        Merges equal tiles, adds merge values to the score, spawns a new
        tile if the board changed, and updates game-over state.
        Returns True if the board changed.
        '''
        if self.game_over:
            return False
        moved = False
        gained = 0
        grid = self.grid
        if direction == 'left':
            for r in range(self.size):
                row, score_gained, row_moved = self._slide_row_left(grid[r])
                grid[r] = row
                gained += score_gained
                moved = moved or row_moved
        elif direction == 'right':
            for r in range(self.size):
                row, score_gained, row_moved = self._slide_row_left(grid[r][::-1])
                row = row[::-1]
                grid[r] = row
                gained += score_gained
                moved = moved or row_moved
        elif direction == 'up':
            transposed = [list(col) for col in zip(*grid)]
            for c in range(self.size):
                col, score_gained, col_moved = self._slide_row_left(transposed[c])
                transposed[c] = col
                gained += score_gained
                moved = moved or col_moved
            grid = [list(row) for row in zip(*transposed)]
            self.grid = grid
        elif direction == 'down':
            transposed = [list(col) for col in zip(*grid)]
            for c in range(self.size):
                col, score_gained, col_moved = self._slide_row_left(transposed[c][::-1])
                transposed[c] = col[::-1]
                gained += score_gained
                moved = moved or col_moved
            grid = [list(row) for row in zip(*transposed)]
            self.grid = grid
        else:
            return False
        if moved:
            self.score += gained
            self._check_win()
            self.spawn_tile()
            if not self.can_move():
                self.game_over = True
        return moved
    def _check_win(self):
        '''Set the won flag the first time the target tile is reached.'''
        if not self.won:
            for row in self.grid:
                if TARGET_TILE in row:
                    self.won = True
                    break
    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------
    def highest_tile(self):
        '''Return the largest tile value currently on the board.'''
        return max(max(row) for row in self.grid)
    def can_move(self):
        '''True if any slide (in any direction) is possible.'''
        # Any empty cell means a move is possible.
        if self.empty_cells():
            return True
        # Otherwise check for horizontally/vertically adjacent equals.
        for r in range(self.size):
            for c in range(self.size):
                value = self.grid[r][c]
                if c + 1 < self.size and self.grid[r][c + 1] == value:
                    return True
                if r + 1 < self.size and self.grid[r + 1][c] == value:
                    return True
        return False