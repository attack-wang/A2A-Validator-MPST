'''
board.py
Defines the Board class, the data model for the Connect Four grid.
Responsibilities:
  * Store the six-row, seven-column grid of discs.
  * Validate column choices (in range and not full).
  * Drop a disc into a column, letting it fall to the lowest empty cell.
  * Detect winning lines of four discs horizontally, vertically,
    and diagonally (both diagonal directions).
  * Detect a full grid (draw condition).
  * Render the board as a string for console display.
'''
# Default dimensions of a standard Connect Four board.
ROW_COUNT = 6
COLUMN_COUNT = 7
# Number of aligned discs required to win.
CONNECT_N = 4
# Symbol used for an empty cell.
EMPTY = ' '
# The four directions a winning line can run in, expressed as
# (row_step, col_step): horizontal, vertical, down-right, up-right.
DIRECTIONS = ((0, 1), (1, 0), (1, 1), (-1, 1))
class Board:
    """Six-row by seven-column Connect Four grid with move and win logic."""
    def __init__(self, rows=ROW_COUNT, cols=COLUMN_COUNT):
        """Create an empty board with the given dimensions."""
        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY for _ in range(cols)] for _ in range(rows)]
    def is_valid_column(self, col):
        """Return True if `col` (0-based) is inside the grid and not full."""
        return 0 <= col < self.cols and self.grid[0][col] == EMPTY
    def get_next_open_row(self, col):
        """Return the lowest empty row in `col`, or None if it is full."""
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == EMPTY:
                return row
        return None
    def drop_disc(self, col, disc):
        """Place `disc` into `col`; return the row it landed in, or None."""
        if not self.is_valid_column(col):
            return None
        row = self.get_next_open_row(col)
        self.grid[row][col] = disc
        return row
    def is_full(self):
        """Return True when every cell is occupied (draw condition)."""
        return all(self.grid[0][col] != EMPTY for col in range(self.cols))
    def find_winning_line(self, disc):
        """Return the cells of a 4-in-a-row line for `disc`, or None.
        Returns a list of (row, col) tuples so the UI can highlight
        the winning discs.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] != disc:
                    continue
                for row_step, col_step in DIRECTIONS:
                    line = []
                    for step in range(CONNECT_N):
                        r = row + row_step * step
                        c = col + col_step * step
                        if 0 <= r < self.rows and 0 <= c < self.cols \
                                and self.grid[r][c] == disc:
                            line.append((r, c))
                        else:
                            break
                    if len(line) == CONNECT_N:
                        return line
        return None
    def check_win(self, disc):
        """Return True if `disc` has any horizontal, vertical or diagonal line of four."""
        return self.find_winning_line(disc) is not None
    def render(self, highlight=None):
        """Return the board as a multi-line string.
        Cells listed in `highlight` (as (row, col) tuples) are drawn
        wrapped in asterisks, e.g. '*X*', to mark a winning line.
        """
        highlight = set(highlight or ())
        separator = '+' + '---+' * self.cols
        header = '|' + '|'.join(f' {c + 1} ' for c in range(self.cols)) + '|'
        lines = [header, separator]
        for r, row in enumerate(self.grid):
            cells = []
            for c, cell in enumerate(row):
                if (r, c) in highlight:
                    cells.append(f'*{cell}*')
                else:
                    cells.append(f' {cell} ')
            lines.append('|' + '|'.join(cells) + '|')
            lines.append(separator)
        return '\n'.join(lines)