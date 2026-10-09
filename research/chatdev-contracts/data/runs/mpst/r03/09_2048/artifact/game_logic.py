'''
game_logic.py
This module implements the core rules of the 2048 game. It manages the
4x4 board state, tile spawning, sliding/merging mechanics for the four
movement directions, score tracking, and game-over detection.
'''
import random
from constants import GRID_SIZE
class Game2048:
    '''Encapsulates the full state and rules of a 2048 game.'''
    def __init__(self, size=GRID_SIZE):
        '''Initialize a new game with an empty board and two starting tiles.'''
        self.size = size
        self.score = 0
        self.highest_tile = 0
        self.game_over = False
        self.reset()
    def reset(self):
        '''Reset the board, score, and status, then spawn two starting tiles.'''
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.highest_tile = 0
        self.game_over = False
        self.add_random_tile()
        self.add_random_tile()
    def get_empty_cells(self):
        '''Return a list of (row, col) tuples for all empty cells.'''
        empty = []
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    empty.append((row, col))
        return empty
    def add_random_tile(self):
        '''Place a new tile (2 with 90% chance, 4 with 10%) in a random empty cell.'''
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return False
        row, col = random.choice(empty_cells)
        value = 2 if random.random() < 0.9 else 4
        self.grid[row][col] = value
        self.highest_tile = max(self.highest_tile, value)
        return True
    def _slide_and_merge_row(self, row):
        '''
        Slide and merge a single row towards the left.
        Returns a tuple (new_row, gained_score) where new_row is the
        transformed row and gained_score is the score earned by merges.
        '''
        # Compact non-zero values to the left
        tiles = [value for value in row if value != 0]
        new_row = []
        gained_score = 0
        index = 0
        while index < len(tiles):
            # Merge adjacent equal tiles (each tile merges at most once per move)
            if index + 1 < len(tiles) and tiles[index] == tiles[index + 1]:
                merged_value = tiles[index] * 2
                new_row.append(merged_value)
                gained_score += merged_value
                index += 2
            else:
                new_row.append(tiles[index])
                index += 1
        # Pad the right side with zeros
        new_row.extend([0] * (self.size - len(new_row)))
        return new_row, gained_score
    def _move_left(self, grid):
        '''Apply a left move to a copy of the grid; returns (new_grid, gained_score).'''
        new_grid = []
        total_score = 0
        for row in grid:
            new_row, gained = self._slide_and_merge_row(row)
            new_grid.append(new_row)
            total_score += gained
        return new_grid, total_score
    def _reverse_rows(self, grid):
        '''Reverse every row (used to turn right moves into left moves).'''
        return [list(reversed(row)) for row in grid]
    def _transpose(self, grid):
        '''Transpose the grid (used to turn up/down moves into left moves).'''
        return [list(row) for row in zip(*grid)]
    def move(self, direction):
        '''
        Perform a move in the given direction ('up', 'down', 'left', 'right').
        Returns True if the board changed (a valid move was made), False otherwise.
        '''
        if self.game_over:
            return False
        working = [row[:] for row in self.grid]
        if direction == 'left':
            working, gained = self._move_left(working)
        elif direction == 'right':
            working, gained = self._move_left(self._reverse_rows(working))
            working = self._reverse_rows(working)
        elif direction == 'up':
            working = self._transpose(working)
            working, gained = self._move_left(working)
            working = self._transpose(working)
        elif direction == 'down':
            working = self._transpose(working)
            working, gained = self._move_left(self._reverse_rows(working))
            working = self._reverse_rows(working)
            working = self._transpose(working)
        else:
            return False
        if working == self.grid:
            return False  # The move did not change the board
        self.grid = working
        self.score += gained
        self.highest_tile = max(self.highest_tile, self._max_tile_value())
        self.add_random_tile()
        if not self.can_move():
            self.game_over = True
        return True
    def _max_tile_value(self):
        '''Return the largest tile value currently on the board.'''
        return max(max(row) for row in self.grid)
    def can_move(self):
        '''Return True if at least one move (in any direction) is possible.'''
        # If there is an empty cell, a move is always possible
        if self.get_empty_cells():
            return True
        # Otherwise check for horizontally adjacent equal tiles
        for row in range(self.size):
            for col in range(self.size - 1):
                if self.grid[row][col] == self.grid[row][col + 1]:
                    return True
        # Check for vertically adjacent equal tiles
        for row in range(self.size - 1):
            for col in range(self.size):
                if self.grid[row][col] == self.grid[row + 1][col]:
                    return True
        return False
    def is_game_over(self):
        '''Return True when the game has ended (no moves remain).'''
        return self.game_over