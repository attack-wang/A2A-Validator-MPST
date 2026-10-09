'''
sudoku_board.py
Core data model for the Sudoku game.
Contains the SudokuBoard class, which stores the 9x9 grid, tracks
which cells are fixed (pre-filled givens), validates placements,
detects rule conflicts (duplicated digits in a row, column or 3x3
box) and determines whether the puzzle has been completed correctly.
'''
GRID_SIZE = 9
BOX_SIZE = 3
EMPTY = 0
class SudokuBoard:
    """Represents a 9x9 Sudoku board and its rules."""
    def __init__(self, puzzle=None):
        """
        Initialize the board.
        Args:
            puzzle: optional 9x9 nested list with ints 0-9
                    (0 means empty cell). If omitted, an empty
                    board is created.
        """
        if puzzle is None:
            puzzle = [[EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self._validate_puzzle_shape(puzzle)
        self.grid = [list(row) for row in puzzle]
        # Cells that came with the puzzle and cannot be modified.
        self.fixed = [[self.grid[r][c] != EMPTY for c in range(GRID_SIZE)]
                      for r in range(GRID_SIZE)]
        # Optional reference solution used to detect "wrong" entries.
        self.solution = None
    @staticmethod
    def _validate_puzzle_shape(puzzle):
        if not isinstance(puzzle, list) or len(puzzle) != GRID_SIZE:
            raise ValueError("Puzzle must be a 9x9 grid.")
        for row in puzzle:
            if not isinstance(row, list) or len(row) != GRID_SIZE:
                raise ValueError("Puzzle must be a 9x9 grid.")
            for cell in row:
                if not isinstance(cell, int) or cell < EMPTY or cell > GRID_SIZE:
                    raise ValueError("Puzzle cells must be integers 0-9.")
    def in_bounds(self, row, col):
        return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE
    def get_value(self, row, col):
        self._check_bounds(row, col)
        return self.grid[row][col]
    def is_fixed(self, row, col):
        self._check_bounds(row, col)
        return self.fixed[row][col]
    def set_value(self, row, col, value):
        """Place a digit (1-9) in an editable cell. Returns True on success."""
        self._check_bounds(row, col)
        if self.fixed[row][col]:
            return False
        if value == EMPTY:
            self.grid[row][col] = EMPTY
            return True
        if not (1 <= value <= GRID_SIZE):
            return False
        self.grid[row][col] = value
        return True
    def clear_value(self, row, col):
        self._check_bounds(row, col)
        if not self.fixed[row][col]:
            self.grid[row][col] = EMPTY
    def is_valid_placement(self, row, col, value):
        """Check whether `value` could be placed at (row, col) without
        duplicating a digit in the same row, column or 3x3 box
        (ignoring the cell itself)."""
        self._check_bounds(row, col)
        if not (1 <= value <= GRID_SIZE):
            return False
        for i in range(GRID_SIZE):
            if i != col and self.grid[row][i] == value:
                return False
            if i != row and self.grid[i][col] == value:
                return False
        box_row, box_col = (row // BOX_SIZE) * BOX_SIZE, (col // BOX_SIZE) * BOX_SIZE
        for r in range(box_row, box_row + BOX_SIZE):
            for c in range(box_col, box_col + BOX_SIZE):
                if (r, c) != (row, col) and self.grid[r][c] == value:
                    return False
        return True
    def get_conflicts(self):
        """Return a set of (row, col) tuples for every cell that shares
        a duplicated digit with another cell in its row, column or box."""
        conflicts = set()
        # rows
        for r in range(GRID_SIZE):
            seen = {}
            for c in range(GRID_SIZE):
                v = self.grid[r][c]
                if v != EMPTY:
                    if v in seen:
                        conflicts.add((r, c))
                        conflicts.add((r, seen[v]))
                    else:
                        seen[v] = c
        # columns
        for c in range(GRID_SIZE):
            seen = {}
            for r in range(GRID_SIZE):
                v = self.grid[r][c]
                if v != EMPTY:
                    if v in seen:
                        conflicts.add((r, c))
                        conflicts.add((seen[v], c))
                    else:
                        seen[v] = r
        # boxes
        for br in range(0, GRID_SIZE, BOX_SIZE):
            for bc in range(0, GRID_SIZE, BOX_SIZE):
                seen = {}
                for r in range(br, br + BOX_SIZE):
                    for c in range(bc, bc + BOX_SIZE):
                        v = self.grid[r][c]
                        if v != EMPTY:
                            if v in seen:
                                conflicts.add((r, c))
                                conflicts.add(seen[v])
                            else:
                                seen[v] = (r, c)
        return conflicts
    def is_complete(self):
        return all(self.grid[r][c] != EMPTY
                   for r in range(GRID_SIZE) for c in range(GRID_SIZE))
    def is_solved(self):
        """True when every cell is filled and no rule is violated."""
        return self.is_complete() and not self.get_conflicts()
    def set_solution(self, solution):
        self.solution = [list(row) for row in solution]
    def get_mistakes(self):
        """Cells whose value differs from the reference solution.
        Returns an empty set when no solution is known."""
        if self.solution is None:
            return set()
        return {(r, c)
                for r in range(GRID_SIZE)
                for c in range(GRID_SIZE)
                if not self.fixed[r][c]
                and self.grid[r][c] != EMPTY
                and self.grid[r][c] != self.solution[r][c]}
    def _check_bounds(self, row, col):
        if not self.in_bounds(row, col):
            raise IndexError("Cell position out of bounds: (%d, %d)" % (row, col))