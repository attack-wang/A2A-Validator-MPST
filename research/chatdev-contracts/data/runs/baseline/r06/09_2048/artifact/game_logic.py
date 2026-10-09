'''
game_logic.py
Core game logic for the 2048 game.
This module implements the Game2048 class, which encapsulates all rules of
the classic 2048 puzzle:
    * A 4x4 grid of tiles.
    * Sliding tiles in one of four directions (up/down/left/right) via
      arrow-key driven moves.
    * Merging pairs of equal tiles into a single tile of doubled value.
    * Spawning a new tile (2 or 4) in a random empty cell after every
      successful move.
    * Score accumulation (each merge adds the merged tile's value).
    * Detection of the game-over state (no moves possible).
    * Tracking of the highest tile value reached during the game.
'''
import random
# Probability that a newly spawned tile is a 2 (otherwise it is a 4).
TWO_PROBABILITY = 0.9
# Direction constants accepted by Game2048.move().
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)
class Game2048:
    '''Model of the 2048 board: grid state, moves, merges, score, game over.'''
    def __init__(self, size=4):
        '''Create a new game with an empty `size` x `size` grid.'''
        self.size = size
        self.reset()
    def reset(self):
        '''Reset the board, score and status, then spawn two starting tiles.'''
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.game_over = False
        self.highest_tile = 0
        self.add_random_tile()
        self.add_random_tile()
        self._update_highest_tile()
    # ------------------------------------------------------------------
    # Board helpers
    # ------------------------------------------------------------------
    def get_empty_cells(self):
        '''Return a list of (row, col) tuples for every empty cell.'''
        return [
            (row, col)
            for row in range(self.size)
            for col in range(self.size)
            if self.grid[row][col] == 0
        ]
    def add_random_tile(self):
        '''Spawn a new tile (2 with 90% chance, else 4) in a random empty cell.'''
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return None
        row, col = random.choice(empty_cells)
        value = 2 if random.random() < TWO_PROBABILITY else 4
        self.grid[row][col] = value
        self._update_highest_tile()
        return (row, col, value)
    def get_highest_tile(self):
        '''Return the highest tile value reached so far in this game.'''
        return self.highest_tile
    def _update_highest_tile(self):
        '''Refresh the highest-tile tracker from the current board.'''
        board_max = max(max(row) for row in self.grid)
        if board_max > self.highest_tile:
            self.highest_tile = board_max
    # ------------------------------------------------------------------
    # Movement / merging
    # ------------------------------------------------------------------
    def move(self, direction):
        '''
        Slide and merge the whole board in `direction`.
        Returns True when at least one tile moved or merged (a legal move);
        in that case a new random tile is spawned. Returns False when the
        move would not change the board (nothing happens).
        '''
        if direction not in ALL_DIRECTIONS:
            raise ValueError(f'Unknown direction: {direction!r}')
        snapshot = [row[:] for row in self.grid]
        # Normalise every direction to a "slide left" operation.
        if direction in (UP, DOWN):
            self.grid = self._transpose(self.grid)
        if direction in (RIGHT, DOWN):
            self.grid = [row[::-1] for row in self.grid]
        gained_score = 0
        for index, row in enumerate(self.grid):
            merged_row, row_score = self._slide_and_merge_row(row)
            self.grid[index] = merged_row
            gained_score += row_score
        # Undo the normalisation transformations.
        if direction in (RIGHT, DOWN):
            self.grid = [row[::-1] for row in self.grid]
        if direction in (UP, DOWN):
            self.grid = self._transpose(self.grid)
        if self.grid == snapshot:
            return False  # Illegal move: board unchanged.
        self.score += gained_score
        self.add_random_tile()
        self._update_highest_tile()
        if not self.can_move():
            self.game_over = True
        return True
    @staticmethod
    def _slide_and_merge_row(row):
        '''
        Slide one row towards index 0, merging equal neighbours once each.
        Returns (new_row, score_gained). Example: [2, 2, 4, 0] ->
        ([4, 4, 0, 0], 4).
        '''
        non_zero = [value for value in row if value != 0]
        merged = []
        score_gained = 0
        index = 0
        while index < len(non_zero):
            if index + 1 < len(non_zero) and non_zero[index] == non_zero[index + 1]:
                merged_value = non_zero[index] * 2
                merged.append(merged_value)
                score_gained += merged_value
                index += 2  # A merged tile cannot merge again this move.
            else:
                merged.append(non_zero[index])
                index += 1
        merged.extend([0] * (len(row) - len(merged)))
        return merged, score_gained
    @staticmethod
    def _transpose(grid):
        '''Return the transpose of a square grid (rows become columns).'''
        return [list(row) for row in zip(*grid)]
    # ------------------------------------------------------------------
    # Game-over detection
    # ------------------------------------------------------------------
    def can_move(self):
        '''Return True when at least one direction changes the board.'''
        if self.get_empty_cells():
            return True  # Any empty cell means tiles can slide.
        # Otherwise a move is possible only if two equal tiles are adjacent.
        for row in range(self.size):
            for col in range(self.size):
                value = self.grid[row][col]
                if col + 1 < self.size and self.grid[row][col + 1] == value:
                    return True
                if row + 1 < self.size and self.grid[row + 1][col] == value:
                    return True
        return False
    def is_game_over(self):
        '''Return True when no moves are possible any more.'''
        return self.game_over