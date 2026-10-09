'''
board.py
Defines the Board class for the Connect Four game. The Board stores the
7x6 grid, validates column choices, drops discs into columns, renders the
board to the console, and detects winning lines (horizontal, vertical,
diagonal) as well as full-grid draw conditions.
'''
class Board:
    """
    Represents the Connect Four grid and the rules for placing discs.
    Attributes:
        rows (int): Number of rows in the grid (default 6).
        cols (int): Number of columns in the grid (default 7).
        grid (list): 2D list of cell symbols ('.', 'X' or 'O').
    """
    EMPTY = '.'
    DISC_ONE = 'X'
    DISC_TWO = 'O'
    def __init__(self, rows=6, cols=7):
        """Create an empty rows x cols grid."""
        self.rows = rows
        self.cols = cols
        self.grid = [[self.EMPTY for _ in range(self.cols)]
                     for _ in range(self.rows)]
    def reset(self):
        """Clear the grid so a new match can start."""
        self.grid = [[self.EMPTY for _ in range(self.cols)]
                     for _ in range(self.rows)]
    def is_valid_column(self, col):
        """
        Return True if col is inside the grid and the column is not full.
        Args:
            col (int): Zero-based column index.
        """
        if not isinstance(col, int):
            return False
        if col < 0 or col >= self.cols:
            return False
        return self.grid[0][col] == self.EMPTY
    def drop_disc(self, col, disc):
        """
        Place a disc into the lowest empty cell of the given column.
        Args:
            col (int): Zero-based column index.
            disc (str): Symbol of the disc being placed ('X' or 'O').
        Returns:
            int: The zero-based row index where the disc landed.
        Raises:
            ValueError: If the column is out of range or already full.
        """
        if not self.is_valid_column(col):
            raise ValueError("Column {} is not available.".format(col + 1))
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == self.EMPTY:
                self.grid[row][col] = disc
                return row
        # Defensive guard: unreachable in normal flow because
        # is_valid_column() already rejects full columns, but kept to
        # guarantee a well-defined failure if invariants are ever broken.
        raise ValueError("Column {} is full.".format(col + 1))
    def is_full(self):
        """Return True when every top cell is occupied (grid is full)."""
        return all(self.grid[0][col] != self.EMPTY
                   for col in range(self.cols))
    def check_win(self, disc, last_row=None, last_col=None):
        """
        Return True if the given disc forms a line of four or more.
        If last_row/last_col are supplied, only lines passing through that
        cell are examined (efficient post-move check); otherwise the whole
        board is scanned.
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        if last_row is None or last_col is None:
            cells = [(r, c)
                     for r in range(self.rows)
                     for c in range(self.cols)
                     if self.grid[r][c] == disc]
        else:
            cells = [(last_row, last_col)]
        for row, col in cells:
            for d_row, d_col in directions:
                count = 1
                count += self._count_direction(row, col, d_row, d_col, disc)
                count += self._count_direction(row, col, -d_row, -d_col, disc)
                if count >= 4:
                    return True
        return False
    def _count_direction(self, row, col, d_row, d_col, disc):
        """Count consecutive discs of `disc` extending from (row, col)."""
        count = 0
        r, c = row + d_row, col + d_col
        while 0 <= r < self.rows and 0 <= c < self.cols \
                and self.grid[r][c] == disc:
            count += 1
            r += d_row
            c += d_col
        return count
    def display(self):
        """Print the grid with column numbers to the console."""
        print()
        print('  ' + ' '.join(str(c + 1) for c in range(self.cols)))
        print('+' + '-' * (2 * self.cols - 1) + '+')
        for row in self.grid:
            print('|' + ' '.join(row) + '|')
        print('+' + '-' * (2 * self.cols - 1) + '+')