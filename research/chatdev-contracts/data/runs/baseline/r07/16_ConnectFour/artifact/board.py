'''
board.py
This module defines the Board class, which models the Connect Four
grid (6 rows x 7 columns). It is responsible for disc placement with
gravity, validation of column choices, win detection across all four
directions, draw detection, and rendering the board to the console.
'''
class Board:
    """Represents the Connect Four playing grid and its rules."""
    ROWS = 6
    COLUMNS = 7
    EMPTY = " "
    WIN_LENGTH = 4
    def __init__(self) -> None:
        """Create an empty 6x7 grid (row 0 is the top row)."""
        self.grid = [
            [self.EMPTY for _ in range(self.COLUMNS)]
            for _ in range(self.ROWS)
        ]
    def reset(self) -> None:
        """Empty every cell of the grid."""
        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                self.grid[row][col] = self.EMPTY
    def is_valid_column(self, column: int) -> bool:
        """
        Check whether a column can accept another disc.
        Args:
            column: 1-based column number chosen by a player.
        Returns:
            True if the column is within range and not full.
        """
        if not isinstance(column, int) or isinstance(column, bool):
            return False
        if column < 1 or column > self.COLUMNS:
            return False
        return self.grid[0][column - 1] == self.EMPTY
    def get_available_row(self, column: int):
        """
        Return the row index where a disc would land in the given
        column (the lowest empty cell), or None if the column is full.
        """
        for row in range(self.ROWS - 1, -1, -1):
            if self.grid[row][column - 1] == self.EMPTY:
                return row
        return None
    def drop_disc(self, column: int, disc: str):
        """
        Place a disc in the given column, letting it fall to the
        lowest empty row.
        Args:
            column: 1-based column number chosen by a player.
            disc: Symbol of the disc to drop.
        Returns:
            Tuple (row, col) with the 0-based landing coordinates.
        Raises:
            ValueError: If the column is out of range or full.
        """
        if not self.is_valid_column(column):
            raise ValueError(f"Cannot drop a disc into column {column}.")
        row = self.get_available_row(column)
        self.grid[row][column - 1] = disc
        return row, column - 1
    def is_full(self) -> bool:
        """Return True when every cell is occupied (draw condition)."""
        return all(
            cell != self.EMPTY
            for row in self.grid
            for cell in row
        )
    def check_win(self, row: int, col: int, disc: str) -> bool:
        """
        Determine whether the disc just placed at (row, col) completes
        a line of at least four identical discs horizontally,
        vertically, or diagonally.
        Args:
            row: 0-based row of the last placed disc.
            col: 0-based column of the last placed disc.
            disc: Symbol of the disc that was placed.
        Returns:
            True if the move produces a winning line.
        """
        directions = [
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (1, 1),   # diagonal (top-left to bottom-right)
            (1, -1),  # diagonal (top-right to bottom-left)
        ]
        for d_row, d_col in directions:
            count = (
                1
                + self._count_direction(row, col, d_row, d_col, disc)
                + self._count_direction(row, col, -d_row, -d_col, disc)
            )
            if count >= self.WIN_LENGTH:
                return True
        return False
    def _count_direction(self, row: int, col: int,
                         d_row: int, d_col: int, disc: str) -> int:
        """Count consecutive matching discs from (row, col) moving in
        the direction (d_row, d_col), excluding the starting cell."""
        count = 0
        r, c = row + d_row, col + d_col
        while (
            0 <= r < self.ROWS
            and 0 <= c < self.COLUMNS
            and self.grid[r][c] == disc
        ):
            count += 1
            r += d_row
            c += d_col
        return count
    def display(self) -> None:
        """Render the current grid with column numbers to the console."""
        labels = "".join(f"  {c} " for c in range(1, self.COLUMNS + 1))
        border = "+" + "---+" * self.COLUMNS
        print()
        print("  " + labels)
        print(" " + border)
        for row in self.grid:
            print(" | " + " | ".join(row) + " |")
            print(" " + border)
        print()