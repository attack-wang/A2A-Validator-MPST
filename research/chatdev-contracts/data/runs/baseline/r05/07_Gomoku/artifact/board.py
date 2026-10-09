'''
Board module for the Gomoku game.
Provides the Board class, which stores the 15x15 grid, validates and
executes stone placements, and detects whether the most recent move
produced an unbroken row of five (or more) stones in any direction.
'''
from config import BOARD_SIZE, EMPTY, WIN_COUNT
class Board:
    '''Represents the Gomoku board: grid storage, move validation and win detection.'''
    def __init__(self, size=BOARD_SIZE):
        '''Create an empty board of the given size (default 15x15).'''
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
    def reset(self):
        '''Clear every intersection so a fresh game can begin.'''
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
    def in_bounds(self, row, col):
        '''Return True if (row, col) lies inside the board.'''
        return 0 <= row < self.size and 0 <= col < self.size
    def is_valid_move(self, row, col):
        '''Return True if (row, col) is inside the board and currently empty.'''
        return self.in_bounds(row, col) and self.grid[row][col] == EMPTY
    def place_stone(self, row, col, player):
        '''Place a stone for `player` at (row, col).
        Returns True on success, False if the move is illegal.'''
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = player
        return True
    def get_stone(self, row, col):
        '''Return the grid code (EMPTY/BLACK/WHITE) at (row, col);
        out-of-bounds positions are treated as empty.'''
        if self.in_bounds(row, col):
            return self.grid[row][col]
        return EMPTY
    def is_full(self):
        '''Return True when no empty intersection remains (a draw).'''
        return all(stone != EMPTY for row in self.grid for stone in row)
    def check_win(self, row, col, player):
        '''Check whether the stone just placed at (row, col) completes an
        unbroken row of at least WIN_COUNT stones.
        Scans the four axes through the last move (horizontal, vertical and
        both diagonals), counting consecutive friendly stones in both
        directions.
        Returns the list of (row, col) positions forming the winning line,
        or an empty list when there is no win.'''
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            line = [(row, col)]
            r, c = row + dr, col + dc          # extend forward
            while self.get_stone(r, c) == player:
                line.append((r, c))
                r += dr
                c += dc
            r, c = row - dr, col - dc          # extend backward
            while self.get_stone(r, c) == player:
                line.append((r, c))
                r -= dr
                c -= dc
            if len(line) >= WIN_COUNT:
                return line
        return []