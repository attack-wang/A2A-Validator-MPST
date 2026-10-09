'''
Pure game logic for 2048, completely independent of any GUI code.
The board is represented as a list of lists of integers, where 0 marks an
empty cell. All 2048 rules are implemented here:
  * Sliding tiles in one of four directions with the arrow keys.
  * Merging pairs of equal tiles (each tile merges at most once per move).
  * Spawning a new tile (2 with 90% probability, 4 otherwise) after every
    successful move.
  * Scoring: every merge adds the value of the newly created tile.
  * Detecting when no further move is possible (game over).
  * Tracking the highest tile value reached during the game.
'''
import random
from constants import GRID_SIZE, TWO_PROBABILITY, INITIAL_TILES
class Game2048:
    '''
    Model of a 2048 game. Holds the board, the current score and the highest
    tile reached, and exposes methods to move/reset the game.
    '''
    def __init__(self, size=GRID_SIZE):
        '''
        Create a new game with an empty `size x size` board and deal the
        initial tiles.
        '''
        self.size = size
        self.reset()
    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def reset(self):
        '''
        Reset the game to its initial state: empty board, zero score and the
        standard two starting tiles.
        '''
        self.board = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.highest_tile = 0
        self.game_over = False
        for _ in range(INITIAL_TILES):
            self._spawn_tile()
    def move(self, direction):
        '''
        Slide and merge all tiles in `direction` ("up", "down", "left" or
        "right"). Returns True if the board changed (a legal move), False
        otherwise. After a legal move a new tile is spawned and the game-over
        state is re-evaluated.
        '''
        if self.game_over:
            return False
        original = [row[:] for row in self.board]
        gained = 0
        if direction == "left":
            for r in range(self.size):
                self.board[r], row_gain = self._slide_row_left(self.board[r])
                gained += row_gain
        elif direction == "right":
            for r in range(self.size):
                self.board[r], row_gain = self._slide_row_left(self.board[r][::-1])
                self.board[r].reverse()
                gained += row_gain
        elif direction == "up":
            self.board = self._transpose(self.board)
            for r in range(self.size):
                self.board[r], row_gain = self._slide_row_left(self.board[r])
                gained += row_gain
            self.board = self._transpose(self.board)
        elif direction == "down":
            self.board = self._transpose(self.board)
            for r in range(self.size):
                self.board[r], row_gain = self._slide_row_left(self.board[r][::-1])
                self.board[r].reverse()
                gained += row_gain
            self.board = self._transpose(self.board)
        else:
            raise ValueError("direction must be 'up', 'down', 'left' or 'right'")
        if self.board == original:
            return False  # Nothing moved: not a legal move.
        self.score += gained
        self._spawn_tile()
        self._refresh_highest_tile()
        if not self.can_move():
            self.game_over = True
        return True
    def can_move(self):
        '''
        Return True if at least one legal move exists (an empty cell or two
        adjacent equal tiles).
        '''
        for r in range(self.size):
            for c in range(self.size):
                value = self.board[r][c]
                if value == 0:
                    return True
                if c + 1 < self.size and self.board[r][c + 1] == value:
                    return True
                if r + 1 < self.size and self.board[r + 1][c] == value:
                    return True
        return False
    def is_game_over(self):
        '''Return True when no moves are possible any more.'''
        return not self.can_move()
    def get_empty_cells(self):
        '''Return a list of (row, column) tuples for all empty cells.'''
        return [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.board[r][c] == 0
        ]
    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _spawn_tile(self):
        '''
        Place a new tile (2 with probability TWO_PROBABILITY, otherwise 4) on
        a random empty cell. Returns True if a tile was placed.
        '''
        empty = self.get_empty_cells()
        if not empty:
            return False
        r, c = random.choice(empty)
        self.board[r][c] = 2 if random.random() < TWO_PROBABILITY else 4
        self._refresh_highest_tile()
        return True
    def _refresh_highest_tile(self):
        '''Update `highest_tile` from the current board contents.'''
        flat = [value for row in self.board for value in row]
        if flat:
            self.highest_tile = max(self.highest_tile, max(flat))
    @staticmethod
    def _slide_row_left(row):
        '''
        Slide and merge a single row towards the left.
        Returns a tuple (new_row, gained_score). Each tile may take part in
        at most one merge per move, matching the official 2048 rules.
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
                i += 2  # The merged tile cannot merge again this move.
            else:
                new_row.append(tiles[i])
                i += 1
        new_row.extend([0] * (len(row) - len(new_row)))
        return new_row, gained
    @staticmethod
    def _transpose(board):
        '''Return the transpose of a square board (rows become columns).'''
        return [list(row) for row in zip(*board)]