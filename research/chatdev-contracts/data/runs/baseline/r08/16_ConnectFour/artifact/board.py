'''
board.py
Defines the Board class for the Connect Four game. The Board stores the
6-row by 7-column grid, validates column choices, drops discs with gravity,
renders the board to the console, and detects winning lines (horizontal,
vertical, and both diagonals) as well as the full-grid draw condition.
'''
from typing import List, Optional
class Board:
    """Represents the Connect Four grid (6 rows x 7 columns)."""
    EMPTY = '.'
    def __init__(self, rows: int = 6, cols: int = 7) -> None:
        """Initialize an empty board with the given dimensions."""
        self.rows: int = rows
        self.cols: int = cols
        self.grid: List[List[str]] = [
            [self.EMPTY for _ in range(cols)] for _ in range(rows)
        ]
    def is_valid_column(self, col: int) -> bool:
        """Return True if col is inside the grid and not already full."""
        return 0 <= col < self.cols and self.grid[0][col] == self.EMPTY
    def drop_disc(self, col: int, disc: str) -> Optional[int]:
        """
        Drop a disc into the chosen column so it falls to the lowest empty
        cell. Return the row index where it landed, or None if the column
        is out of range or already full.
        """
        if not self.is_valid_column(col):
            return None
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == self.EMPTY:
                self.grid[row][col] = disc
                return row
        return None
    def check_win(self, row: int, col: int, disc: str) -> bool:
        """
        Return True if the disc just placed at (row, col) completes a line
        of at least four identical discs horizontally, vertically, or
        diagonally.
        """
        directions = [
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (1, 1),   # diagonal (down-right / up-left)
            (1, -1),  # diagonal (down-left / up-right)
        ]
        return any(
            self._count_consecutive(row, col, disc, d_row, d_col) >= 4
            for d_row, d_col in directions
        )
    def _count_consecutive(
        self,
        row: int,
        col: int,
        disc: str,
        delta_row: int,
        delta_col: int,
    ) -> int:
        """
        Count the consecutive discs of `disc` along the line through
        (row, col) with step (delta_row, delta_col), including the disc at
        (row, col) itself.
        """
        count = 1
        # Scan in the positive direction.
        r, c = row + delta_row, col + delta_col
        while 0 <= r < self.rows and 0 <= c < self.cols \
                and self.grid[r][c] == disc:
            count += 1
            r += delta_row
            c += delta_col
        # Scan in the negative direction.
        r, c = row - delta_row, col - delta_col
        while 0 <= r < self.rows and 0 <= c < self.cols \
                and self.grid[r][c] == disc:
            count += 1
            r -= delta_row
            c -= delta_col
        return count
    def is_full(self) -> bool:
        """Return True when every cell is occupied (draw condition)."""
        return all(self.grid[0][c] != self.EMPTY for c in range(self.cols))
    def display(self) -> None:
        """Print the current board state with 1-based column numbers."""
        header = ' '.join(str(c + 1) for c in range(self.cols))
        print('\n' + header)
        for row_cells in self.grid:
            print(' '.join(row_cells))
        print('-' * len(header))