'''
Core game logic for the 2048 game.
This module contains the Game2048 class, which manages the 4x4 board,
tile spawning, slide/merge mechanics for the four movement directions,
score tracking, highest-tile tracking, and game-over detection. It is
completely independent of any rendering code, so it can be unit-tested
or reused with a different front end.
'''
import random
class Game2048:
    '''
    Encapsulates all rules and state of a standard game of 2048.
    Attributes:
        grid_size:      Side length of the square board (4 for standard 2048).
        starting_tiles: Number of tiles placed when a game begins.
        two_probability: Chance a spawned tile is a 2 (otherwise a 4).
        board:          2D list of ints; 0 represents an empty cell.
        score:          Points accumulated from tile merges so far.
        highest_tile:   Largest tile value currently on the board.
        game_over:      True when no further moves are possible.
    '''
    def __init__(self, grid_size=4, starting_tiles=2, two_probability=0.9):
        '''Create a fresh board and place the initial random tiles.'''
        self.grid_size = grid_size
        self.starting_tiles = starting_tiles
        self.two_probability = two_probability
        self.score = 0
        self.highest_tile = 0
        self.game_over = False
        self.board = [[0] * grid_size for _ in range(grid_size)]
        for _ in range(starting_tiles):
            self.spawn_tile()
    def reset(self):
        '''Restore the game to its initial state (empty board, zero score).'''
        self.score = 0
        self.highest_tile = 0
        self.game_over = False
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        for _ in range(self.starting_tiles):
            self.spawn_tile()
    def spawn_tile(self):
        '''Place a 2 (90%) or 4 (10%) in a random empty cell, if any exists.'''
        empty_cells = [(row, col) for row in range(self.grid_size)
                       for col in range(self.grid_size)
                       if self.board[row][col] == 0]
        if not empty_cells:
            return
        row, col = random.choice(empty_cells)
        self.board[row][col] = 2 if random.random() < self.two_probability else 4
        self._update_highest_tile()
    def move(self, direction):
        '''
        Slide and merge all tiles toward the given direction
        ('up', 'down', 'left' or 'right').
        Returns True when the board changed: the score is updated and a
        new random tile spawns. Returns False for an ineffective move,
        leaving the board untouched (standard 2048 behaviour), and also
        when the game is already over.
        '''
        if self.game_over:
            return False
        # Express every direction as a left-slide on the rows of a
        # transformed copy of the board.
        if direction == 'left':
            grid = [row[:] for row in self.board]
        elif direction == 'right':
            grid = [row[::-1] for row in self.board]
        elif direction == 'up':
            grid = [list(col) for col in zip(*self.board)]
        elif direction == 'down':
            grid = [list(col)[::-1] for col in zip(*self.board)]
        else:
            return False
        new_grid = []
        gained = 0
        moved = False
        for row in grid:
            new_row, row_gained = self._slide_row_left(row)
            gained += row_gained
            moved = moved or new_row != row
            new_grid.append(new_row)
        if not moved:
            return False  # Ineffective move: no slide, no merge, no spawn.
        # Undo the transformation and write the result back to the board.
        if direction == 'left':
            self.board = new_grid
        elif direction == 'right':
            self.board = [row[::-1] for row in new_grid]
        elif direction == 'up':
            self.board = [list(col) for col in zip(*new_grid)]
        else:  # 'down'
            self.board = [list(col) for col in zip(*new_grid)][::-1]
        self.score += gained
        self._update_highest_tile()
        self.spawn_tile()
        self.game_over = not self._moves_available()
        return True
    @staticmethod
    def _slide_row_left(row):
        '''
        Compress one row to the left, merging each pair of equal
        neighbours at most once. Returns (new_row, points_gained).
        '''
        tiles = [value for value in row if value != 0]
        new_row = []
        gained = 0
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                merged = tiles[i] * 2
                new_row.append(merged)
                gained += merged
                i += 2
            else:
                new_row.append(tiles[i])
                i += 1
        new_row.extend([0] * (len(row) - len(new_row)))
        return new_row, gained
    def _moves_available(self):
        '''True when any empty cell or any adjacent equal pair exists.'''
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if self.board[row][col] == 0:
                    return True
                if (col + 1 < self.grid_size
                        and self.board[row][col] == self.board[row][col + 1]):
                    return True
                if (row + 1 < self.grid_size
                        and self.board[row][col] == self.board[row + 1][col]):
                    return True
        return False
    def _update_highest_tile(self):
        '''Refresh highest_tile from the current board contents.'''
        max_tile = max(max(row) for row in self.board)
        if max_tile > self.highest_tile:
            self.highest_tile = max_tile