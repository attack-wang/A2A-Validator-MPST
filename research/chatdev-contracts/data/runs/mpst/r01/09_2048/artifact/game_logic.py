'''
game_logic.py
Pure game rules for 2048: board state, tile spawning, sliding/merging,
score tracking, win detection and end-of-game detection. This module has
no dependency on any GUI library, so the rules can be tested or reused
independently of the presentation layer.
'''
import random
from constants import GRID_SIZE, NEW_TILE_VALUES
# Direction constants
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
VALID_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)
# Tile value that triggers the "won" flag
WINNING_TILE = 2048
class Game2048:
    '''
    Holds the 4x4 board and implements the rules of 2048.
    Attributes:
        grid:      2D list of ints (0 means an empty cell).
        score:     Current score; increases by the value of every merge.
        game_over: True when no move is possible anymore.
        won:       True once a 2048 tile has been created.
    '''
    def __init__(self, grid_size=GRID_SIZE):
        self.grid_size = grid_size
        self.reset()
    # ------------------------------------------------------------------
    # State management
    # ------------------------------------------------------------------
    def reset(self):
        '''Start a fresh game: empty board, zero score, two random tiles.'''
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.game_over = False
        self.won = False
        self.spawn_tile()
        self.spawn_tile()
    def get_empty_cells(self):
        '''Return a list of (row, col) tuples for every empty cell.'''
        return [
            (r, c)
            for r in range(self.grid_size)
            for c in range(self.grid_size)
            if self.grid[r][c] == 0
        ]
    def spawn_tile(self):
        '''
        Place a new tile (2 with 80% chance, 4 with 20% chance) on a
        random empty cell. Returns True if a tile was placed.
        '''
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return False
        row, col = random.choice(empty_cells)
        self.grid[row][col] = random.choice(NEW_TILE_VALUES)
        return True
    def get_highest_tile(self):
        '''Return the value of the highest tile currently on the board.'''
        return max(max(row) for row in self.grid)
    # ------------------------------------------------------------------
    # Move handling
    # ------------------------------------------------------------------
    def move(self, direction):
        '''
        Slide and merge all tiles in the given direction.
        Returns True when the board changed (a legal move was played);
        in that case a new tile is spawned, the win flag is checked and
        the game-over state is re-evaluated. Returns False when the move
        changes nothing (or the game is already over).
        '''
        if direction not in VALID_DIRECTIONS or self.game_over:
            return False
        snapshot = [row[:] for row in self.grid]
        if direction == LEFT:
            self._move_rows(reverse=False)
        elif direction == RIGHT:
            self._move_rows(reverse=True)
        elif direction == UP:
            self._move_columns(reverse=False)
        elif direction == DOWN:
            self._move_columns(reverse=True)
        if self.grid == snapshot:
            return False  # Nothing moved: not a legal move
        self.spawn_tile()
        if not self.won and self.get_highest_tile() >= WINNING_TILE:
            self.won = True
        if not self.can_move():
            self.game_over = True
        return True
    def _move_rows(self, reverse):
        '''Apply slide+merge to every row (reverse=True means "right").'''
        for r in range(self.grid_size):
            line = self.grid[r][::-1] if reverse else self.grid[r]
            merged, gained = self._slide_and_merge(line)
            self.grid[r] = merged[::-1] if reverse else merged
            self.score += gained
    def _move_columns(self, reverse):
        '''Apply slide+merge to every column (reverse=True means "down").'''
        for c in range(self.grid_size):
            line = [self.grid[r][c] for r in range(self.grid_size)]
            if reverse:
                line.reverse()
            merged, gained = self._slide_and_merge(line)
            if reverse:
                merged.reverse()
            for r in range(self.grid_size):
                self.grid[r][c] = merged[r]
            self.score += gained
    @staticmethod
    def _slide_and_merge(line):
        '''
        Slide a single line toward index 0 and merge equal neighbours.
        Each tile may merge at most once per move, exactly like the
        original game. Returns (new_line, score_gained).
        '''
        tiles = [value for value in line if value != 0]
        new_line = []
        score_gained = 0
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                merged_value = tiles[i] * 2
                new_line.append(merged_value)
                score_gained += merged_value
                i += 2
            else:
                new_line.append(tiles[i])
                i += 1
        new_line.extend([0] * (len(line) - len(new_line)))
        return new_line, score_gained
    # ------------------------------------------------------------------
    # End-of-game detection
    # ------------------------------------------------------------------
    def can_move(self):
        '''True when at least one move (any direction) is possible.'''
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                value = self.grid[r][c]
                if value == 0:
                    return True  # An empty cell can always be filled by a slide
                if c + 1 < self.grid_size and self.grid[r][c + 1] == value:
                    return True  # Horizontal merge possible
                if r + 1 < self.grid_size and self.grid[r + 1][c] == value:
                    return True  # Vertical merge possible
        return False