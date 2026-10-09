'''
board.py
Defines the Board class for the Connect Four game.
The Board stores the 6-row by 7-column grid, drops discs into the
lowest empty cell of a column, renders the board (optionally
highlighting a winning line), and detects winning lines of four
and full-board conditions.
'''
ROWS = 6
COLUMNS = 7
EMPTY = "."
CONNECT = 4
class Board:
    """Represents the 7-column, 6-row Connect Four grid."""
    def __init__(self, rows=ROWS, columns=COLUMNS):
        """Create an empty grid of the given size."""
        self.rows = rows
        self.columns = columns
        self.grid = [[EMPTY for _ in range(columns)] for _ in range(rows)]
    def display(self, highlight=None):
        """Print the board; cells in `highlight` are wrapped in brackets."""
        highlight = highlight or set()
        # Column numbers are printed so each digit sits above its column.
        print(" " + "   ".join(str(col + 1) for col in range(self.columns)))
        for row in range(self.rows):
            cells = []
            for col in range(self.columns):
                cell = self.grid[row][col]
                if (row, col) in highlight:
                    cells.append(f"[{cell}]")
                else:
                    cells.append(f" {cell} ")
            print(" ".join(cells))
        print(" " + "-" * (4 * self.columns - 1))
        print()
    def is_valid_column(self, column):
        """Return True if `column` is inside the grid and not full."""
        return 0 <= column < self.columns and self.grid[0][column] == EMPTY
    def drop_disc(self, column, disc):
        """Place `disc` in `column` at the lowest empty row; return its row."""
        if not self.is_valid_column(column):
            raise ValueError(f"Column {column + 1} is not available.")
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][column] == EMPTY:
                self.grid[row][column] = disc
                return row
        raise ValueError(f"Column {column + 1} is already full.")
    def is_full(self):
        """Return True when every top-row cell is occupied."""
        return all(self.grid[0][col] != EMPTY for col in range(self.columns))
    def find_winning_line(self, disc):
        """Return the set of (row, col) cells of a 4-in-a-row of `disc`, else None."""
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))  # horizontal, vertical, \, /
        for row in range(self.rows):
            for col in range(self.columns):
                for dr, dc in directions:
                    line = []
                    for step in range(CONNECT):
                        r, c = row + dr * step, col + dc * step
                        if 0 <= r < self.rows and 0 <= c < self.columns \
                                and self.grid[r][c] == disc:
                            line.append((r, c))
                        else:
                            break
                    if len(line) == CONNECT:
                        return set(line)
        return None