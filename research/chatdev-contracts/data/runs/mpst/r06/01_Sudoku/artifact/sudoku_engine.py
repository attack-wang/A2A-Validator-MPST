'''
sudoku_engine.py
Core game logic for the classic Sudoku puzzle game.
This module contains the SudokuBoard class, which models the 9x9 grid,
validates placements against Sudoku rules (each row, column and 3x3
subgrid must contain the digits 1-9 exactly once), detects conflicts,
and determines whether the puzzle has been completed correctly.
'''
class SudokuBoard:
    """Model of a 9x9 Sudoku board with rule validation helpers."""
    GRID_SIZE = 9
    SUBGRID_SIZE = 3
    def __init__(self, puzzle=None):
        """Initialize the board..."""
        if puzzle is not None:
            self._validate_puzzle_shape(puzzle)
            self.grid = [[int(puzzle[r][c]) for c in range(self.GRID_SIZE)]
                         for r in range(self.GRID_SIZE)]
        else:
            self.grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self.given = [[self.grid[r][c] != 0 for c in range(self.GRID_SIZE)]
                      for r in range(self.GRID_SIZE)]
    @staticmethod
    def _validate_puzzle_shape(puzzle):
        """Ensure the supplied puzzle is a 9x9 structure."""
        if len(puzzle) != SudokuBoard.GRID_SIZE:
            raise ValueError("Puzzle must have exactly 9 rows.")
        for row in puzzle:
            if len(row) != SudokuBoard.GRID_SIZE:
                raise ValueError("Each puzzle row must have exactly 9 cells.")
    def get_cell(self, row, col):
        """Return the value stored at (row, col). 0 means empty."""
        self._check_indices(row, col)
        return self.grid[row][col]
    def set_cell(self, row, col, value):
        """Store a value at (row, col)..."""
        self._check_indices(row, col)
        if value != 0 and not self.is_valid_value(value):
            raise ValueError("Cell value must be 0 (empty) or a digit 1-9.")
        self.grid[row][col] = value
        return self.is_cell_consistent(row, col)
    def is_given(self, row, col):
        """Return True if the cell was pre-filled and must not be edited."""
        self._check_indices(row, col)
        return self.given[row][col]
    @classmethod
    def is_valid_value(cls, value):
        """Return True if value is an integer in the range 0-9."""
        return isinstance(value, int) and 0 <= value <= 9
    @staticmethod
    def _check_indices(row, col):
        """Raise IndexError if row or col is outside the 9x9 grid."""
        if not (0 <= row < SudokuBoard.GRID_SIZE and 0 <= col < SudokuBoard.GRID_SIZE):
            raise IndexError("Row and column must be in range 0-8.")
    def is_cell_consistent(self, row, col):
        """Return True if the value at (row, col) duplicates nothing in its row, column or 3x3 subgrid."""
        self._check_indices(row, col)
        value = self.grid[row][col]
        if value == 0:
            return True
        box_row = (row // self.SUBGRID_SIZE) * self.SUBGRID_SIZE
        box_col = (col // self.SUBGRID_SIZE) * self.SUBGRID_SIZE
        for i in range(self.GRID_SIZE):
            if i != col and self.grid[row][i] == value:
                return False
            if i != row and self.grid[i][col] == value:
                return False
        for r in range(box_row, box_row + self.SUBGRID_SIZE):
            for c in range(box_col, box_col + self.SUBGRID_SIZE):
                if (r, c) != (row, col) and self.grid[r][c] == value:
                    return False
        return True
    def find_conflicts(self):
        """Return a set of (row, col) tuples for every cell that violates Sudoku rules."""
        return {(r, c)
                for r in range(self.GRID_SIZE)
                for c in range(self.GRID_SIZE)
                if self.grid[r][c] != 0 and not self.is_cell_consistent(r, c)}
    def count_empty_cells(self):
        """Return the number of cells still empty (value 0)."""
        return sum(1 for r in range(self.GRID_SIZE)
                     for c in range(self.GRID_SIZE)
                     if self.grid[r][c] == 0)
    def is_complete(self):
        """Return True when every cell is filled and no rule is violated."""
        if self.count_empty_cells() != 0:
            return False
        return not self.find_conflicts()
    def reset_to_givens(self):
        """Erase every non-given cell, restoring the original puzzle."""
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                if not self.given[r][c]:
                    self.grid[r][c] = 0