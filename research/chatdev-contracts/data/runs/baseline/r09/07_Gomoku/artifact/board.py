'''
board.py
Defines the Board class which manages the 15x15 Gomoku board state,
including stone placement, move validation, and win detection.
'''
from constants import EMPTY, BLACK, WHITE
class Board:
    '''Represents the Gomoku board and its state.'''
    def __init__(self, size=15):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
    def reset(self):
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.grid[row][col] is EMPTY
    def place_stone(self, row, col, color):
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = color
        return True
    def get_cell(self, row, col):
        return self.grid[row][col]
    def is_full(self):
        return all(cell is not EMPTY for row in self.grid for cell in row)
    def check_win(self, row, col):
        '''Check whether the stone just placed at (row, col) completes
        an unbroken line of five or more stones of the same color.'''
        color = self.grid[row][col]
        if color is EMPTY:
            return False
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for dr, dc in directions:
            count = 1
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == color:
                count += 1
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == color:
                count += 1
                r -= dr
                c -= dc
            if count >= 5:
                return True
        return False
    def get_winning_line(self, row, col):
        '''Return the list of (row, col) positions forming the winning line
        through (row, col), or None if there is no winning line.'''
        color = self.grid[row][col]
        if color is EMPTY:
            return None
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for dr, dc in directions:
            line = [(row, col)]
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == color:
                line.append((r, c))
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == color:
                line.insert(0, (r, c))
                r -= dr
                c -= dc
            if len(line) >= 5:
                return line
        return None