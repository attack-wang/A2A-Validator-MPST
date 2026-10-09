'''
game_logic.py
Core game logic for the 2048 game.
This module is completely independent of any user-interface code. It manages
the 4x4 board state, tile spawning, sliding/merging mechanics, score
tracking, the highest tile reached, and game-over detection.
'''
import random
class Game2048:
    '''Encapsulates the full state and rules of a standard 2048 game.'''
    def __init__(self, size=4):
        self.size = size
        self.reset()
    def reset(self):
        '''Reset the board to the initial state with two random tiles.'''
        self.board = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.highest_tile = 0
        self.won = False
        self.spawn_tile()
        self.spawn_tile()
    # ------------------------------------------------------------------
    # Board helpers
    # ------------------------------------------------------------------
    def get_empty_cells(self):
        '''Return a list of (row, col) tuples for every empty cell.'''
        return [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.board[r][c] == 0
        ]
    def spawn_tile(self):
        '''Place a new tile (2 with 90% chance, 4 with 10%) in a random empty cell.'''
        empty = self.get_empty_cells()
        if not empty:
            return False
        r, c = random.choice(empty)
        self.board[r][c] = 2 if random.random() < 0.9 else 4
        self.highest_tile = max(self.highest_tile, self.board[r][c])
        return True
    # ------------------------------------------------------------------
    # Core movement mechanics
    # ------------------------------------------------------------------
    @staticmethod
    def _slide_row_left(row):
        '''
        Slide and merge a single row towards the left.
        Returns a tuple (new_row, gained_score). Each tile can merge at most
        once per move, following the official 2048 rules.
        '''
        tiles = [v for v in row if v != 0]
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
        new_row += [0] * (len(row) - len(new_row))
        return new_row, gained
    def _apply_move(self, board, direction):
        '''
        Apply a slide/merge to a copy of the board.
        Returns (new_board, gained_score, moved) where `moved` indicates
        whether any tile changed position or value.
        '''
        if direction == 'left':
            def transform(b):
                return [row[:] for row in b]
            def inverse(b):
                return [row[:] for row in b]
        elif direction == 'right':
            def transform(b):
                return [row[::-1] for row in b]
            def inverse(b):
                return [row[::-1] for row in b]
        elif direction == 'up':
            def transform(b):
                return [list(col) for col in zip(*b)]
            def inverse(b):
                return [list(col) for col in zip(*b)]
        elif direction == 'down':
            def transform(b):
                # Transpose, then reverse each row: the bottom of every column
                # comes first, so "slide left" becomes "slide down".
                return [list(col)[::-1] for col in zip(*b)]
            def inverse(b):
                # The inverse of (transpose + reverse rows) is
                # (reverse rows + transpose), NOT the same operation again.
                return [list(col) for col in zip(*[row[::-1] for row in b])]
        else:
            raise ValueError(f'Unknown direction: {direction}')
        oriented = transform(board)
        new_board = []
        gained_total = 0
        for row in oriented:
            new_row, gained = self._slide_row_left(row)
            new_board.append(new_row)
            gained_total += gained
        restored = inverse(new_board)
        moved = restored != board
        return restored, gained_total, moved
    def move(self, direction):
        '''
        Perform a move in one of the four directions.
        Returns True if the board changed (a valid move was made); in that
        case a new tile is spawned and the score is updated.
        '''
        if direction not in ('up', 'down', 'left', 'right'):
            raise ValueError(f'Unknown direction: {direction}')
        new_board, gained, moved = self._apply_move(self.board, direction)
        if not moved:
            return False
        self.board = new_board
        self.score += gained
        self.highest_tile = max(
            self.highest_tile, max(max(row) for row in self.board)
        )
        if not self.won and any(2048 in row for row in self.board):
            self.won = True
        self.spawn_tile()
        return True
    # ------------------------------------------------------------------
    # Game-over detection
    # ------------------------------------------------------------------
    def can_move(self):
        '''Return True if at least one move in any direction is possible.'''
        # Any empty cell means a move is possible.
        if self.get_empty_cells():
            return True
        # Otherwise check for horizontally/vertically adjacent equal tiles.
        for r in range(self.size):
            for c in range(self.size):
                value = self.board[r][c]
                if c + 1 < self.size and self.board[r][c + 1] == value:
                    return True
                if r + 1 < self.size and self.board[r + 1][c] == value:
                    return True
        return False
    def is_game_over(self):
        '''The game ends when no moves are possible.'''
        return not self.can_move()
    def get_highest_tile(self):
        '''Return the highest tile value currently on the board.'''
        return max(max(row) for row in self.board)