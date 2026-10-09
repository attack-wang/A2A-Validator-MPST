'''
Game logic module for the 2048 game.
Contains the Game2048 class, which manages the 4x4 grid, tile sliding and
merging, random tile spawning, score tracking, highest-tile tracking, and
game-over detection. This module has no Pygame dependency so the core
rules can be tested independently of the presentation layer.
'''
import random
class Game2048:
    '''Implements the rules and state of a standard 4x4 game of 2048.'''
    def __init__(self, size=4):
        '''Create an empty grid and spawn the two starting tiles.'''
        self.size = size
        self.grid = [[0] * size for _ in range(size)]
        self.score = 0
        self.highest_tile = 0
        self.game_over = False
        self.spawn_tile()
        self.spawn_tile()
    def get_empty_cells(self):
        '''Return a list of (row, col) tuples marking every empty cell.'''
        return [(r, c)
                for r in range(self.size)
                for c in range(self.size)
                if self.grid[r][c] == 0]
    def spawn_tile(self):
        '''Place a new tile in a random empty cell (2 with 90% chance, 4 otherwise).
        Returns True if a tile was spawned, False if the grid is full.
        '''
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return False
        row, col = random.choice(empty_cells)
        self.grid[row][col] = 2 if random.random() < 0.9 else 4
        self.highest_tile = max(self.highest_tile, self.grid[row][col])
        return True
    @staticmethod
    def _slide_row_left(row):
        '''Slide and merge one row toward the left.
        Returns a tuple (new_row, score_gained, moved) where:
          new_row      -- the row after sliding/merging
          score_gained -- points earned from merges in this row
          moved        -- True if the row changed at all
        '''
        tiles = [value for value in row if value != 0]
        merged = []
        score_gained = 0
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                doubled = tiles[i] * 2
                merged.append(doubled)
                score_gained += doubled
                i += 2  # a merged tile cannot merge again this move
            else:
                merged.append(tiles[i])
                i += 1
        merged.extend([0] * (len(row) - len(merged)))
        moved = merged != list(row)
        return merged, score_gained, moved
    def move(self, direction):
        '''Slide all tiles in the given direction ('up', 'down', 'left', 'right').
        Merges equal neighbours, adds the merge points to the score, spawns a
        new random tile if the board changed, and flags game over when no
        further move exists. Returns True if the board changed.
        '''
        if self.game_over:
            return False
        moved = False
        score_gained = 0
        if direction in ('left', 'right'):
            for r in range(self.size):
                row = self.grid[r]
                if direction == 'right':
                    row = row[::-1]
                new_row, gained, row_moved = self._slide_row_left(row)
                if direction == 'right':
                    new_row = new_row[::-1]
                self.grid[r] = new_row
                score_gained += gained
                moved = moved or row_moved
        elif direction in ('up', 'down'):
            for c in range(self.size):
                column = [self.grid[r][c] for r in range(self.size)]
                if direction == 'down':
                    column = column[::-1]
                new_column, gained, col_moved = self._slide_row_left(column)
                if direction == 'down':
                    new_column = new_column[::-1]
                for r in range(self.size):
                    self.grid[r][c] = new_column[r]
                score_gained += gained
                moved = moved or col_moved
        else:
            return False  # unknown direction: ignore
        if moved:
            self.score += score_gained
            self.spawn_tile()
            # Catch tiles created by merges (spawn_tile only sees the new tile)
            self.highest_tile = max(self.highest_tile, self.get_highest_tile())
            if not self.can_move():
                self.game_over = True
        return moved
    def get_highest_tile(self):
        '''Return the largest tile value currently on the grid.'''
        return max(max(row) for row in self.grid)
    def can_move(self):
        '''Return True while at least one legal move (slide or merge) exists.'''
        if self.get_empty_cells():
            return True
        for r in range(self.size):
            for c in range(self.size - 1):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return True
        for r in range(self.size - 1):
            for c in range(self.size):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False