'''
game_logic.py
Core 2048 game logic: grid state, tile spawning, movement/merging,
score tracking, and game-over detection.
'''
import random
# Direction constants
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
VALID_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)
class Game2048:
    '''Represents the state and rules of a 4x4 2048 game.'''
    def __init__(self, size=4):
        self.size = size
        self.reset()
    def reset(self):
        '''Reset the game to its initial state with two random tiles.'''
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.highest_tile = 0
        self.game_over = False
        self._add_random_tile()
        self._add_random_tile()
    def get_empty_cells(self):
        '''Return a list of (row, col) tuples for all empty cells.'''
        cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    cells.append((r, c))
        return cells
    def _add_random_tile(self):
        '''Place a new tile (2 with 90% chance, 4 with 10%) in a random empty cell.'''
        empty = self.get_empty_cells()
        if not empty:
            return
        r, c = random.choice(empty)
        value = 2 if random.random() < 0.9 else 4
        self.grid[r][c] = value
        if value > self.highest_tile:
            self.highest_tile = value
    def move(self, direction):
        '''
        Slide and merge all tiles in the given direction.
        Returns True if the grid changed (a valid move was made).
        '''
        if direction not in VALID_DIRECTIONS:
            raise ValueError(f"Invalid direction: {direction}")
        original = [row[:] for row in self.grid]
        moved_grid, gained = self._apply_move(direction)
        self.grid = moved_grid
        self.score += gained
        # update highest tile
        for row in self.grid:
            for v in row:
                if v > self.highest_tile:
                    self.highest_tile = v
        if moved_grid != original:
            self._add_random_tile()
            if self.is_game_over():
                self.game_over = True
            return True
        return False
    def _apply_move(self, direction):
        '''Apply the move; returns (new_grid, score_gained).'''
        # Build lines in the direction of movement, each line processed as a left-slide
        lines = self._extract_lines(direction)
        new_lines = []
        total_gain = 0
        for line in lines:
            new_line, gain = self._slide_and_merge(line)
            new_lines.append(new_line)
            total_gain += gain
        new_grid = self._place_lines(new_lines, direction)
        return new_grid, total_gain
    def _extract_lines(self, direction):
        '''Extract rows/columns oriented so that index 0 is closest to the movement edge.'''
        size = self.size
        lines = []
        if direction == LEFT:
            lines = [self.grid[r][:] for r in range(size)]
        elif direction == RIGHT:
            lines = [self.grid[r][::-1] for r in range(size)]
        elif direction == UP:
            lines = [[self.grid[r][c] for r in range(size)] for c in range(size)]
        elif direction == DOWN:
            lines = [[self.grid[size - 1 - r][c] for r in range(size)] for c in range(size)]
        return lines
    def _place_lines(self, lines, direction):
        '''Place processed lines back into a new grid.'''
        size = self.size
        new_grid = [[0] * size for _ in range(size)]
        if direction == LEFT:
            for r in range(size):
                new_grid[r] = lines[r][:]
        elif direction == RIGHT:
            for r in range(size):
                new_grid[r] = lines[r][::-1]
        elif direction == UP:
            for c in range(size):
                for r in range(size):
                    new_grid[r][c] = lines[c][r]
        elif direction == DOWN:
            for c in range(size):
                for r in range(size):
                    new_grid[size - 1 - r][c] = lines[c][r]
        return new_grid
    @staticmethod
    def _slide_and_merge(line):
        '''
        Slide non-zero values left and merge equal neighbors once per move.
        Returns (new_line, score_gained).
        '''
        tiles = [v for v in line if v != 0]
        new_line = []
        gained = 0
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                merged = tiles[i] * 2
                new_line.append(merged)
                gained += merged
                i += 2
            else:
                new_line.append(tiles[i])
                i += 1
        new_line.extend([0] * (len(line) - len(new_line)))
        return new_line, gained
    def can_move(self):
        '''Return True if at least one move (in any direction) changes the grid.'''
        # If any empty cell exists, a move is possible
        if self.get_empty_cells():
            return True
        # Check horizontal merges
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return True
        # Check vertical merges
        for c in range(self.size):
            for r in range(self.size - 1):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False
    def is_game_over(self):
        '''The game is over when no moves are possible.'''
        return not self.can_move()
    def get_highest_tile(self):
        '''Return the highest tile value currently on the grid.'''
        highest = 0
        for row in self.grid:
            for v in row:
                if v > highest:
                    highest = v
        return highest