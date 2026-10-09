'''
board.py
Board module for the Gomoku game. Provides the Board class, which stores
the 15x15 grid, validates and applies moves, detects a win of five in a
row (horizontal, vertical, or diagonal), and detects a full-board draw.
'''
from constants import BOARD_SIZE, EMPTY
class Board:
    '''
    Represents the Gomoku board.
    The board is a square grid of BOARD_SIZE x BOARD_SIZE cells. Each cell
    holds EMPTY (0), BLACK (1), or WHITE (2). Stones are placed on the
    intersections of the grid, which this implementation models directly
    as grid cells.
    '''
    def __init__(self):
        '''Initialize an empty 15x15 board.'''
        self.size = BOARD_SIZE
        self.grid = [[EMPTY] * self.size for _ in range(self.size)]
        self.last_move = None  # (row, col) of the most recently placed stone
    def reset(self):
        '''Clear every cell so a fresh game can start.'''
        self.grid = [[EMPTY] * self.size for _ in range(self.size)]
        self.last_move = None
    def in_bounds(self, row, col):
        '''Return True if (row, col) lies inside the board.'''
        return 0 <= row < self.size and 0 <= col < self.size
    def is_valid_move(self, row, col):
        '''A move is valid when it is inside the board and the cell is empty.'''
        return self.in_bounds(row, col) and self.grid[row][col] == EMPTY
    def place_stone(self, row, col, player):
        '''
        Place a stone for `player` at (row, col).
        Returns True if the stone was placed, False if the move is invalid
        (out of bounds or the cell is already occupied).
        '''
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = player
        self.last_move = (row, col)
        return True
    def check_win(self, row, col, player):
        '''
        Check whether the stone just placed at (row, col) by `player`
        completes five or more in a row.
        Scans the four axes through the placed stone (horizontal, vertical,
        and both diagonals), counting consecutive friendly stones in both
        directions.
        Returns the list of (row, col) cells forming the winning line if
        there is a win, otherwise None.
        '''
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            cells = [(row, col)]
            # Walk in the positive direction of the axis.
            r, c = row + dr, col + dc
            while self.in_bounds(r, c) and self.grid[r][c] == player:
                cells.append((r, c))
                r += dr
                c += dc
            # Walk in the negative direction of the axis.
            r, c = row - dr, col - dc
            while self.in_bounds(r, c) and self.grid[r][c] == player:
                cells.append((r, c))
                r -= dr
                c -= dc
            if len(cells) >= 5:
                return cells
        return None
    def is_full(self):
        '''Return True when no empty cell remains (the game is a draw).'''
        return all(cell != EMPTY for row in self.grid for cell in row)
    def get_stone(self, row, col):
        '''Return the player occupying (row, col), or EMPTY.'''
        if self.in_bounds(row, col):
            return self.grid[row][col]
        return EMPTY