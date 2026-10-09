'''
game_logic.py
Implements the core rules of tic-tac-toe: board state management, move
validation, move tracking, win detection across rows/columns/diagonals,
and draw detection. This module is fully independent of the user interface.
'''
from constants import BOARD_SIZE, EMPTY, PLAYER_X, PLAYER_O
class Board:
    '''Represents the 3x3 tic-tac-toe board and enforces the game rules.'''
    def __init__(self):
        '''Create an empty board ready for a new game.'''
        self.reset()
    def reset(self):
        '''Clear every cell and the move history to start a fresh game.'''
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.move_history = []
    def is_valid_move(self, row, col):
        '''Return True if (row, col) lies inside the board and is empty.'''
        return (
            0 <= row < BOARD_SIZE
            and 0 <= col < BOARD_SIZE
            and self.grid[row][col] == EMPTY
        )
    def make_move(self, row, col, player):
        '''
        Place `player`'s symbol at (row, col) if the move is legal.
        Returns True when the move is applied, False otherwise. Every
        accepted move is recorded in the move history.
        '''
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = player
        self.move_history.append((player, row, col))
        return True
    def get_cell(self, row, col):
        '''Return the symbol stored at (row, col).'''
        return self.grid[row][col]
    def is_full(self):
        '''Return True when no empty cells remain (draw condition).'''
        return all(
            self.grid[row][col] != EMPTY
            for row in range(BOARD_SIZE)
            for col in range(BOARD_SIZE)
        )
    def get_available_moves(self):
        '''Return a list of (row, col) tuples for every empty cell.'''
        return [
            (row, col)
            for row in range(BOARD_SIZE)
            for col in range(BOARD_SIZE)
            if self.grid[row][col] == EMPTY
        ]
    def get_move_history(self):
        '''Return a copy of all moves made so far as (player, row, col).'''
        return list(self.move_history)
    def check_winner(self):
        '''
        Evaluate all rows, columns, and diagonals for a completed line.
        Returns:
            (winner, line): `winner` is PLAYER_X or PLAYER_O when a player
            has completed a line, otherwise None; `line` is the list of
            (row, col) cells forming the winning line, otherwise None.
        '''
        lines = self._all_lines()
        for line in lines:
            first_row, first_col = line[0]
            first_symbol = self.grid[first_row][first_col]
            if first_symbol == EMPTY:
                continue
            if all(self.grid[row][col] == first_symbol for row, col in line):
                return first_symbol, line
        return None, None
    @staticmethod
    def _all_lines():
        '''Return every possible winning line on the board as cell lists.'''
        lines = []
        # Three rows.
        for row in range(BOARD_SIZE):
            lines.append([(row, col) for col in range(BOARD_SIZE)])
        # Three columns.
        for col in range(BOARD_SIZE):
            lines.append([(row, col) for row in range(BOARD_SIZE)])
        # Main diagonal and anti-diagonal.
        lines.append([(i, i) for i in range(BOARD_SIZE)])
        lines.append([(i, BOARD_SIZE - 1 - i) for i in range(BOARD_SIZE)])
        return lines