'''
game_logic.py
Core game logic for the Tic-Tac-Toe application.
The GameBoard class encapsulates the 3x3 board state and all rules of
the game: validating and applying moves, detecting a winner (rows,
columns, and both diagonals), detecting a draw, listing available
moves, and locating the winning line so the interface can highlight it.
'''
class GameBoard:
    '''Represents the 3x3 Tic-Tac-Toe board and its rules.'''
    BOARD_SIZE = 3
    EMPTY = " "
    def __init__(self):
        '''Create an empty 3x3 board ready for a new game.'''
        self._init_grid()
    def _init_grid(self):
        '''(Re)build the internal grid filled with empty cells.'''
        self.grid = [[self.EMPTY for _ in range(self.BOARD_SIZE)]
                     for _ in range(self.BOARD_SIZE)]
    def reset(self):
        '''Clear every cell so a fresh game can begin.'''
        self._init_grid()
    def is_valid_move(self, row, col):
        '''
        Return True if (row, col) lies inside the board and the cell
        is still empty; otherwise return False.
        '''
        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
            return self.grid[row][col] == self.EMPTY
        return False
    def make_move(self, row, col, symbol):
        '''
        Place `symbol` ("X" or "O") at (row, col).
        Returns True when the move is applied, False when the cell is
        out of range or already occupied.
        '''
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = symbol
        return True
    def get_cell(self, row, col):
        '''Return the symbol stored at (row, col).'''
        return self.grid[row][col]
    def is_full(self):
        '''Return True when no empty cells remain (draw condition).'''
        for row in self.grid:
            if self.EMPTY in row:
                return False
        return True
    def check_winner(self):
        '''
        Return the winning symbol ("X" or "O") if either player has
        completed a row, column, or diagonal; otherwise return None.
        Delegates to get_winning_line() so win detection has a single
        source of truth.
        '''
        line = self.get_winning_line()
        if line is not None:
            first_row, first_col = line[0]
            return self.grid[first_row][first_col]
        return None
    def get_winning_line(self):
        '''
        Return the list of (row, col) coordinates forming the winning
        line, or None when there is no winner yet.
        '''
        for line in self._all_lines():
            symbols = [self.grid[r][c] for r, c in line]
            if symbols[0] != self.EMPTY and symbols[0] == symbols[1] == symbols[2]:
                return line
        return None
    def get_available_moves(self):
        '''Return a list of (row, col) tuples for every empty cell.'''
        return [(r, c)
                for r in range(self.BOARD_SIZE)
                for c in range(self.BOARD_SIZE)
                if self.grid[r][c] == self.EMPTY]
    def _all_lines(self):
        '''Return every 3-cell line that can win the game.'''
        lines = []
        # Rows
        for r in range(self.BOARD_SIZE):
            lines.append([(r, 0), (r, 1), (r, 2)])
        # Columns
        for c in range(self.BOARD_SIZE):
            lines.append([(0, c), (1, c), (2, c)])
        # Main diagonal
        lines.append([(0, 0), (1, 1), (2, 2)])
        # Anti-diagonal
        lines.append([(0, 2), (1, 1), (2, 0)])
        return lines