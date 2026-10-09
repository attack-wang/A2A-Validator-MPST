'''
game.py
Core game logic for the 2048 game: grid management, tile merging,
scoring, and game-over detection.
'''
import random
from constants import GRID_SIZE, TILE_PROBABILITY_TWO, UP, DOWN, LEFT, RIGHT
class Game:
    '''Represents the state and rules of a 2048 game.'''
    def __init__(self):
        self.reset()
    def reset(self):
        '''Reset the game to its initial state with two random tiles.'''
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.game_over = False
        self.spawn_tile()
        self.spawn_tile()
    def spawn_tile(self):
        '''Place a new tile (2 or 4) in a random empty cell.'''
        empty_cells = [(r, c) for r in range(GRID_SIZE)
                       for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if not empty_cells:
            return
        r, c = random.choice(empty_cells)
        self.grid[r][c] = 2 if random.random() < TILE_PROBABILITY_TWO else 4
    def get_highest_tile(self):
        '''Return the highest tile value currently on the grid.'''
        return max(max(row) for row in self.grid)
    def can_move(self):
        '''Return True if any move (up/down/left/right) can change the grid.'''
        # An empty cell always means at least one move is possible.
        for row in self.grid:
            if 0 in row:
                return True
        # Board is full: a move is possible only if two adjacent tiles are equal.
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = self.grid[r][c]
                if (c + 1 < GRID_SIZE and self.grid[r][c + 1] == value) or \
                   (r + 1 < GRID_SIZE and self.grid[r + 1][c] == value):
                    return True
        return False
    def move(self, direction):
        '''
        Slide and merge all tiles in the given direction.
        Returns True if the grid changed (valid move), False otherwise.
        '''
        original = [row[:] for row in self.grid]
        self._transform_for_direction(direction)
        score_gained = 0
        for i in range(GRID_SIZE):
            self.grid[i], gained = self._slide_and_merge(self.grid[i])
            score_gained += gained
        self._undo_transform(direction)
        if self.grid != original:
            self.score += score_gained
            self.spawn_tile()
            if not self.can_move():
                self.game_over = True
            return True
        return False
    def _transform_for_direction(self, direction):
        '''Transform the grid so every direction can be processed as a left move.'''
        if direction == UP:
            self.grid = [list(row) for row in zip(*self.grid)]
        elif direction == DOWN:
            # Transpose, then reverse each row: columns become rows read
            # bottom-to-top, so a "left" slide moves tiles toward the bottom.
            self.grid = [list(row) for row in zip(*self.grid)]
            self.grid = [row[::-1] for row in self.grid]
        elif direction == RIGHT:
            self.grid = [row[::-1] for row in self.grid]
    def _undo_transform(self, direction):
        '''Undo the transformation applied by _transform_for_direction.'''
        if direction == UP:
            self.grid = [list(row) for row in zip(*self.grid)]
        elif direction == DOWN:
            # Exact inverse of the DOWN transform: reverse each row, then transpose.
            self.grid = [row[::-1] for row in self.grid]
            self.grid = [list(row) for row in zip(*self.grid)]
        elif direction == RIGHT:
            self.grid = [row[::-1] for row in self.grid]
    @staticmethod
    def _slide_and_merge(line):
        '''
        Slide and merge a single line toward index 0.
        Returns a tuple (new_line, score_gained) so the caller can update the score.
        '''
        tiles = [v for v in line if v != 0]
        merged = []
        score_gained = 0
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                merged.append(tiles[i] * 2)
                score_gained += tiles[i] * 2
                i += 2  # Each tile may merge at most once per move.
            else:
                merged.append(tiles[i])
                i += 1
        merged.extend([0] * (GRID_SIZE - len(merged)))
        return merged, score_gained