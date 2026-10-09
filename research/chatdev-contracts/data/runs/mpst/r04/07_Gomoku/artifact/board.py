'''
board.py
Defines the Board class: it stores the 15x15 grid, validates and applies
stone placements, and detects a five-in-a-row win in every direction.
'''
from constants import (
    BOARD_SIZE,
    STONES_TO_WIN,
    EMPTY,
    DIRECTIONS,
)
class Board:
    '''
    Represents the Gomoku playing field and the pure game logic that
    operates on it (placement validation, win detection, draw detection).
    '''
    def __init__(self, size=BOARD_SIZE):
        '''Create an empty board with the given number of intersections.'''
        self.size = size
        self.grid = self._empty_grid()
    def _empty_grid(self):
        '''Return a fresh size x size grid filled with EMPTY cells.'''
        return [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
    def reset(self):
        '''Clear every cell so a brand new match can begin.'''
        self.grid = self._empty_grid()
    def is_inside(self, row, col):
        '''Return True when (row, col) lies within the board limits.'''
        return 0 <= row < self.size and 0 <= col < self.size
    def is_valid_move(self, row, col):
        '''Return True when (row, col) is inside the board and empty.'''
        return self.is_inside(row, col) and self.grid[row][col] == EMPTY
    def place_stone(self, row, col, player):
        '''
        Put a stone of `player` on (row, col).
        Return True when the move was applied, False when it is invalid.
        '''
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = player
        return True
    def get_stone(self, row, col):
        '''Return the value at (row, col): EMPTY, BLACK or WHITE.'''
        if self.is_inside(row, col):
            return self.grid[row][col]
        return None
    def is_full(self):
        '''Return True when no empty cell remains (the match is a draw).'''
        for row in self.grid:
            for cell in row:
                if cell == EMPTY:
                    return False
        return True
    def get_winning_line(self, row, col, player):
        '''
        Determine whether the stone just placed at (row, col) completes
        at least five aligned stones for `player`.
        Return the ordered list of (row, col) cells forming the winning
        line, or None when the move does not win the game.
        '''
        for d_row, d_col in DIRECTIONS:
            cells = [(row, col)]
            # Walk towards the positive end of the direction.
            r, c = row + d_row, col + d_col
            while self.is_inside(r, c) and self.grid[r][c] == player:
                cells.append((r, c))
                r += d_row
                c += d_col
            # Walk towards the negative end of the direction.
            r, c = row - d_row, col - d_col
            while self.is_inside(r, c) and self.grid[r][c] == player:
                cells.insert(0, (r, c))
                r -= d_row
                c -= d_col
            if len(cells) >= STONES_TO_WIN:
                return cells
        return None