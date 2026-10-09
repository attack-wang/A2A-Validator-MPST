'''
board.py
Defines the Board class for the Gomoku game: a square grid that stores
stones, validates moves, and detects five-in-a-row wins and draws.
Stone colors are encoded as integer constants (EMPTY, BLACK, WHITE).
'''
EMPTY = 0
BLACK = 1
WHITE = 2
class Board:
    '''Represents the Gomoku playing grid and its core rules logic.'''
    def __init__(self, size=15):
        '''Create an empty size x size board.'''
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
    def is_valid_move(self, row, col):
        '''Return True if (row, col) is inside the board and empty.'''
        return (
            0 <= row < self.size
            and 0 <= col < self.size
            and self.grid[row][col] == EMPTY
        )
    def place_stone(self, row, col, stone):
        '''Place a stone at (row, col); return True on success.'''
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = stone
        return True
    def check_win(self, row, col):
        '''Return True if the stone at (row, col) completes five in a row.
        Checks the four axes through the last move (horizontal, vertical,
        and both diagonals) by counting consecutive same-colored stones
        in both directions from the placed stone.
        '''
        stone = self.grid[row][col]
        if stone == EMPTY:
            return False
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for dr, dc in directions:
            count = 1
            # Count consecutive stones in the positive direction.
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == stone:
                count += 1
                r += dr
                c += dc
            # Count consecutive stones in the negative direction.
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == stone:
                count += 1
                r -= dr
                c -= dc
            if count >= 5:
                return True
        return False
    def is_full(self):
        '''Return True when no empty cells remain (a draw).'''
        for row_cells in self.grid:
            if EMPTY in row_cells:
                return False
        return True
    def get_cell(self, row, col):
        '''Return the value stored at (row, col).'''
        return self.grid[row][col]