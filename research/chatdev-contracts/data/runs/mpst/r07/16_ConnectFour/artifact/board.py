'''
board.py
Defines the Board class for the Connect Four game.
The Board encapsulates the six-row by seven-column grid, provides disc
placement with gravity (discs stack from the bottom up), validates column
choices, detects winning lines (horizontal, vertical, and both diagonals),
detects a full-grid draw condition, and renders the board to the console.
'''
# Game dimensions and win length (standard Connect Four rules).
ROWS = 6
COLS = 7
CONNECT = 4
EMPTY = ' '
class Board:
    '''Represents the Connect Four grid and all board-related logic.'''
    def __init__(self, rows=ROWS, cols=COLS):
        '''Create an empty grid with the given dimensions.'''
        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]
    def is_valid_column(self, column):
        '''Return True if `column` (1-based) is in range and not full.'''
        if not isinstance(column, int) or isinstance(column, bool):
            return False
        if column < 1 or column > self.cols:
            return False
        return self.grid[0][column - 1] == EMPTY
    def drop_disc(self, column, disc):
        '''
        Place `disc` into the given 1-based column, letting it fall to the
        lowest empty cell. Return the 0-based row where it landed, or None
        if the move is invalid.
        '''
        if not self.is_valid_column(column):
            return None
        col_index = column - 1
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col_index] == EMPTY:
                self.grid[row][col_index] = disc
                return row
        return None
    def is_full(self):
        '''Return True when every cell is occupied (draw condition).'''
        return all(self.grid[0][c] != EMPTY for c in range(self.cols))
    def check_win(self, row, col, disc):
        '''
        Check whether the disc just placed at 0-based (row, col) completes
        a line of at least CONNECT discs. Return the list of (row, col)
        cells forming the line (for highlighting), or None if no win.
        '''
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            cells = [(row, col)]
            for sign in (1, -1):
                r, c = row + dr * sign, col + dc * sign
                while (0 <= r < self.rows and 0 <= c < self.cols
                       and self.grid[r][c] == disc):
                    cells.append((r, c))
                    r += dr * sign
                    c += dc * sign
            if len(cells) >= CONNECT:
                return cells
        return None
    def render(self, highlight=None):
        '''
        Print the board with column numbers. Cells listed in `highlight`
        (an iterable of (row, col) tuples) are wrapped in brackets to mark
        the winning line.
        '''
        highlight = set(highlight) if highlight else set()
        header = ''.join(f' {c} ' for c in range(1, self.cols + 1))
        separator = '-' * (self.cols * 3 + 2)
        print(header)
        print(separator)
        for r in range(self.rows):
            cells = []
            for c in range(self.cols):
                disc = self.grid[r][c]
                if (r, c) in highlight:
                    cells.append(f'[{disc}]')
                else:
                    cells.append(f' {disc} ')
            print('|' + '|'.join(cells) + '|')
        print(separator)