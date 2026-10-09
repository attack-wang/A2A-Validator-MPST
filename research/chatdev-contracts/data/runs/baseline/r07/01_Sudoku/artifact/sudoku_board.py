'''
sudoku_board.py
Board model for the Sudoku game: stores the puzzle, the player's entries and
the fixed clues, and provides rule checking (conflicts, completion).
'''
EMPTY = 0
class SudokuBoard:
    """Represents the 9x9 Sudoku board, its fixed clues and player entries."""
    def __init__(self, puzzle, solution=None):
        """Build a board from a 9x9 puzzle (0 = empty) and an optional solution."""
        self.puzzle = [list(row) for row in puzzle]
        self.solution = [list(row) for row in solution] if solution is not None else None
        self.grid = [list(row) for row in puzzle]
        self.fixed = [[self.puzzle[r][c] != EMPTY for c in range(9)] for r in range(9)]
    @staticmethod
    def _box_index(row, col):
        """Return the index (0-8) of the 3x3 box containing (row, col)."""
        return (row // 3) * 3 + col // 3
    def is_fixed(self, row, col):
        """True if the cell holds an immutable puzzle clue."""
        return self.fixed[row][col]
    def get_value(self, row, col):
        """Return the current value of the cell (0 = empty)."""
        return self.grid[row][col]
    def set_value(self, row, col, value):
        """Set a player value; refuses fixed cells and out-of-range values."""
        if self.is_fixed(row, col):
            return False
        # NOTE: bool is a subclass of int in Python, so reject it explicitly
        if not isinstance(value, int) or isinstance(value, bool) or value < 0 or value > 9:
            return False
        self.grid[row][col] = value
        return True
    def clear_value(self, row, col):
        """Clear a player-entered cell (fixed cells are protected)."""
        return self.set_value(row, col, EMPTY)
    def is_valid_placement(self, row, col, value):
        """Would placing value at (row, col) break Sudoku rules, ignoring the
        current content of the cell?"""
        if value == EMPTY:
            return True
        for c in range(9):
            if c != col and self.grid[row][c] == value:
                return False
        for r in range(9):
            if r != row and self.grid[r][col] == value:
                return False
        br, bc = (row // 3) * 3, (col // 3) * 3
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if (r, c) != (row, col) and self.grid[r][c] == value:
                    return False
        return True
    def find_conflicts(self):
        """Return a set of (row, col) coordinates involved in a rule violation
        (duplicate digit in a row, column, or 3x3 box). Empty cells are ignored."""
        conflicts = set()
        def _scan(cells):
            """Mark every duplicate occurrence inside an iterable of (row, col) pairs."""
            seen = {}
            for r, c in cells:
                v = self.grid[r][c]
                if v == EMPTY:
                    continue
                if v in seen:
                    conflicts.add((r, c))
                    conflicts.add(seen[v])
                else:
                    seen[v] = (r, c)
        for r in range(9):                      # rows
            _scan(((r, c) for c in range(9)))
        for c in range(9):                      # columns
            _scan(((r, c) for r in range(9)))
        for br in (0, 3, 6):                    # 3x3 boxes
            for bc in (0, 3, 6):
                _scan(((r, c) for r in range(br, br + 3) for c in range(bc, bc + 3)))
        return conflicts
    def count_empty(self):
        """Return the number of still-empty cells."""
        return sum(1 for r in range(9) for c in range(9) if self.grid[r][c] == EMPTY)
    def is_complete(self):
        """True when every cell is filled and no Sudoku rule is violated."""
        if self.count_empty() > 0:
            return False
        return not self.find_conflicts()
    def matches_solution(self):
        """True if the grid equals the stored solution (None if no solution)."""
        if self.solution is None:
            return None
        return self.grid == self.solution
    def find_incorrect_cell(self):
        """Return (row, col) of the first empty or wrong cell, or None."""
        for r in range(9):
            for c in range(9):
                if self.solution is not None:
                    if self.grid[r][c] != self.solution[r][c]:
                        return (r, c)
                elif self.grid[r][c] == EMPTY:
                    return (r, c)
        return None