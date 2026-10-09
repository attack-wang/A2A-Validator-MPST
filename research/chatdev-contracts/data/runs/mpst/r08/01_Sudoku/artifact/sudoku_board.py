'''
sudoku_board.py
Model of the Sudoku board: stores the puzzle, the player's current state,
and provides validation, mistake detection, and completion checking.
'''
class SudokuBoard:
    """Represents the Sudoku game state and rule logic."""
    def __init__(self, puzzle, solution):
        self.puzzle = [row[:] for row in puzzle]
        self.solution = [row[:] for row in solution]
        self.grid = [row[:] for row in puzzle]  # current player state
    def is_fixed(self, row, col):
        """True if the cell was pre-filled in the original puzzle."""
        return self.puzzle[row][col] != 0
    def get_value(self, row, col):
        """Return the current value at (row, col); 0 means empty."""
        return self.grid[row][col]
    def set_value(self, row, col, value):
        """Set a player value in an editable cell. Returns True on success."""
        if self.is_fixed(row, col):
            return False
        if value is None:
            self.grid[row][col] = 0
            return True
        try:
            value = int(value)
        except (TypeError, ValueError):
            return False
        if not 1 <= value <= 9:
            return False
        self.grid[row][col] = value
        return True
    def clear_value(self, row, col):
        """Erase the player's value at (row, col) if the cell is editable."""
        if not self.is_fixed(row, col):
            self.grid[row][col] = 0
    def has_conflict(self, row, col):
        """True if the value at (row, col) conflicts with row/col/box peers."""
        value = self.grid[row][col]
        if value == 0:
            return False
        # Row
        for c in range(9):
            if c != col and self.grid[row][c] == value:
                return True
        # Column
        for r in range(9):
            if r != row and self.grid[r][col] == value:
                return True
        # 3x3 box
        br, bc = 3 * (row // 3), 3 * (col // 3)
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if (r, c) != (row, col) and self.grid[r][c] == value:
                    return True
        return False
    def find_mistakes(self):
        """Return a list of (row, col) cells that conflict with Sudoku rules."""
        return [(r, c) for r in range(9) for c in range(9)
                if self.grid[r][c] != 0 and self.has_conflict(r, c)]
    def find_empty_cells(self):
        """Return a list of (row, col) cells that are still empty."""
        return [(r, c) for r in range(9) for c in range(9) if self.grid[r][c] == 0]
    def is_complete(self):
        """True when every cell is filled and no rule conflicts exist."""
        return not self.find_empty_cells() and not self.find_mistakes()
    def is_cell_correct(self, row, col):
        """True if the cell matches the known solution (0 counts as incorrect)."""
        return self.grid[row][col] == self.solution[row][col]
    def reveal_solution(self):
        """Replace the player's grid with the stored solution."""
        self.grid = [row[:] for row in self.solution]