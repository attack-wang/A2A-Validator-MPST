'''
board.py
Defines the Board class, which manages the Connect Four grid: disc
placement with gravity, column validation, and win/draw detection.
'''
from typing import Iterable, List, Optional, Tuple
from config import ROWS, COLUMNS, CONNECT, EMPTY
class Board:
    '''Represents the Connect Four grid and enforces the placement rules.'''
    def __init__(self, rows: int = ROWS, columns: int = COLUMNS, connect: int = CONNECT) -> None:
        '''Create an empty grid with the given dimensions and connect target.'''
        self.rows = rows
        self.columns = columns
        self.connect = connect
        self.grid = [[EMPTY for _ in range(columns)] for _ in range(rows)]
    def is_valid_column(self, column: int) -> bool:
        '''Return True if the 0-based column index is inside the grid.'''
        return 0 <= column < self.columns
    def is_column_full(self, column: int) -> bool:
        '''Return True if the column can no longer accept a disc.
        Out-of-range columns are treated as not full; callers that need
        range validation should use is_valid_column or can_accept_disc.
        '''
        if not self.is_valid_column(column):
            return False
        return self.grid[0][column] != EMPTY
    def get_next_open_row(self, column: int) -> Optional[int]:
        '''Return the lowest empty row index of a column, or None if full.'''
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][column] == EMPTY:
                return row
        return None
    def can_accept_disc(self, column: int) -> bool:
        '''Return True if a disc may be dropped into the column.
        Convenience helper combining range and fullness checks; kept as
        part of the Board's public API for external callers and tests.
        '''
        return self.is_valid_column(column) and not self.is_column_full(column)
    def drop_disc(self, column: int, disc: str) -> int:
        '''Drop a disc into a column and return the row it landed in.
        Raises:
            ValueError: If the column is out of range or already full.
        '''
        if not self.is_valid_column(column):
            raise ValueError(f'Column {column + 1} is out of range (1-{self.columns}).')
        row = self.get_next_open_row(column)
        if row is None:
            raise ValueError(f'Column {column + 1} is already full.')
        self.grid[row][column] = disc
        return row
    def is_full(self) -> bool:
        '''Return True when every cell of the grid is occupied (draw).'''
        return all(cell != EMPTY for row in self.grid for cell in row)
    def check_win_from(self, row: int, column: int, disc: str) -> Optional[List[Tuple[int, int]]]:
        '''Return the coordinates of a winning line through (row, column), or None.
        Checks horizontal, vertical, and both diagonal directions starting
        from the last placed disc.
        '''
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for step_row, step_col in directions:
            line = [(row, column)]
            for sign in (1, -1):
                next_row = row + sign * step_row
                next_col = column + sign * step_col
                while (0 <= next_row < self.rows
                        and 0 <= next_col < self.columns
                        and self.grid[next_row][next_col] == disc):
                    line.append((next_row, next_col))
                    next_row += sign * step_row
                    next_col += sign * step_col
            if len(line) >= self.connect:
                return line
        return None
    def check_win(self, disc: str) -> Optional[List[Tuple[int, int]]]:
        '''Scan the whole grid for any winning line made of the given disc.
        Convenience helper that searches every occupied cell; kept as part
        of the Board's public API for external callers and tests.
        '''
        for row in range(self.rows):
            for column in range(self.columns):
                if self.grid[row][column] == disc:
                    line = self.check_win_from(row, column, disc)
                    if line is not None:
                        return line
        return None
    def render(self, highlight: Optional[Iterable[Tuple[int, int]]] = None) -> str:
        '''Return the grid as a string; cells in `highlight` are wrapped in parentheses.'''
        highlight = set(highlight) if highlight else set()
        separator = '+' + '+'.join(['---'] * self.columns) + '+'
        header = ' ' + ' '.join(f'{number:^3}' for number in range(1, self.columns + 1))
        lines = [header, separator]
        for row_index, row in enumerate(self.grid):
            cells = []
            for col_index, cell in enumerate(row):
                if (row_index, col_index) in highlight:
                    cells.append(f'({cell})')
                else:
                    cells.append(f' {cell} ')
            lines.append('|' + '|'.join(cells) + '|')
        lines.append(separator)
        return '\n'.join(lines)