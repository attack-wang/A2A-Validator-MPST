'''
sudoku_board.py
Core game-state module for the Sudoku application.
Stores the fixed puzzle clues, the player's current entries and the
hidden solution, and implements the Sudoku rules: move validation,
conflict (mistake) detection, hints and completion checking.
'''
import random
class SudokuBoard:
    """Model of a Sudoku game board (rules and state, no GUI code)."""
    GRID_SIZE = 9
    BOX_SIZE = 3
    EMPTY = 0
    def __init__(self, puzzle, solution):
        """Initialize the board from a puzzle and its solution.
        Args:
            puzzle (list[list[int]]): 9x9 grid, 0 for empty cells.
            solution (list[list[int]]): 9x9 fully solved grid.
        """
        self.puzzle = [list(row) for row in puzzle]
        self.solution = [list(row) for row in solution]
        # Player entries start empty everywhere
        self.entries = [[self.EMPTY] * self.GRID_SIZE
                        for _ in range(self.GRID_SIZE)]
        # Cells that came with the puzzle are fixed and not editable
        self.fixed = [[self.puzzle[r][c] != self.EMPTY
                       for c in range(self.GRID_SIZE)]
                      for r in range(self.GRID_SIZE)]
    # ------------------------------------------------------------------
    # Cell queries
    # ------------------------------------------------------------------
    def is_fixed_cell(self, row, col):
        """Return True if (row, col) is a pre-filled puzzle clue."""
        return self.fixed[row][col]
    def get_value(self, row, col):
        """Return the value currently shown at (row, col).
        Fixed clue cells return the puzzle value; all other cells
        return the player's entry (0 if empty).
        """
        if self.fixed[row][col]:
            return self.puzzle[row][col]
        return self.entries[row][col]
    def get_solution_value(self, row, col):
        """Return the correct solution value for (row, col)."""
        return self.solution[row][col]
    def is_cell_empty(self, row, col):
        """Return True if (row, col) currently shows no digit."""
        return self.get_value(row, col) == self.EMPTY
    # ------------------------------------------------------------------
    # Moves
    # ------------------------------------------------------------------
    def set_value(self, row, col, value):
        """Place the player's digit at (row, col).
        Args:
            value (int): digit 1-9, or 0/None to clear the cell.
        Returns:
            bool: True if the value was accepted, False if the cell is
                  fixed or the value is out of range.
        """
        if self.fixed[row][col]:
            return False
        if value is None:
            value = self.EMPTY
        if value != self.EMPTY and not (1 <= value <= 9):
            return False
        self.entries[row][col] = value
        return True
    def clear_cell(self, row, col):
        """Erase the player's entry at (row, col) (fixed cells untouched)."""
        if not self.fixed[row][col]:
            self.entries[row][col] = self.EMPTY
    def clear_user_entries(self):
        """Erase every player entry, keeping the original clues."""
        self.entries = [[self.EMPTY] * self.GRID_SIZE
                        for _ in range(self.GRID_SIZE)]
    # ------------------------------------------------------------------
    # Rules
    # ------------------------------------------------------------------
    def is_valid_placement(self, row, col, value):
        """Check whether `value` may be placed at (row, col) right now.
        The cell's own current value is ignored so replacing an entry
        with the same digit is not reported as conflicting with itself.
        """
        if value == self.EMPTY:
            return True
        # Row check (excluding the cell itself)
        for c in range(self.GRID_SIZE):
            if c != col and self.get_value(row, c) == value:
                return False
        # Column check (excluding the cell itself)
        for r in range(self.GRID_SIZE):
            if r != row and self.get_value(r, col) == value:
                return False
        # 3x3 box check (excluding the cell itself)
        box_row = (row // self.BOX_SIZE) * self.BOX_SIZE
        box_col = (col // self.BOX_SIZE) * self.BOX_SIZE
        for r in range(box_row, box_row + self.BOX_SIZE):
            for c in range(box_col, box_col + self.BOX_SIZE):
                if (r, c) != (row, col) and self.get_value(r, c) == value:
                    return False
        return True
    def find_conflicts(self):
        """Return a set of (row, col) cells that violate Sudoku rules.
        A cell conflicts when its shown value duplicates the same digit
        in its row, column or 3x3 box. All cells sharing the duplicate
        digit are reported, so the player sees every offending cell.
        """
        conflicts = set()
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                value = self.get_value(r, c)
                if value == self.EMPTY:
                    continue
                if not self.is_valid_placement(r, c, value):
                    conflicts.add((r, c))
        return conflicts
    def find_mistakes(self):
        """Return a set of (row, col) player entries that differ from
        the unique solution (definitive mistakes)."""
        mistakes = set()
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                if (not self.fixed[r][c]
                        and self.entries[r][c] != self.EMPTY
                        and self.entries[r][c] != self.solution[r][c]):
                    mistakes.add((r, c))
        return mistakes
    def count_mistakes(self):
        """Return how many player entries are wrong."""
        return len(self.find_mistakes())
    # ------------------------------------------------------------------
    # Completion / hints
    # ------------------------------------------------------------------
    def is_board_full(self):
        """Return True when every cell shows a digit."""
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                if self.get_value(r, c) == self.EMPTY:
                    return False
        return True
    def is_solved(self):
        """Return True when the board is full and matches the solution."""
        if not self.is_board_full():
            return False
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                if self.get_value(r, c) != self.solution[r][c]:
                    return False
        return True
    def get_hint(self):
        """Return (row, col, correct_value) for a random empty/incorrect cell."""
        candidates = [(r, c) for r in range(9) for c in range(9)
                      if not self.fixed[r][c]
                      and self.entries[r][c] != self.solution[r][c]]
        if not candidates:
            return None
        row, col = random.choice(candidates)
        return (row, col, self.solution[row][col])
    def reveal_solution(self):
        """Fill every non-fixed cell with the correct solution value."""
        for r in range(9):
            for c in range(9):
                if not self.fixed[r][c]:
                    self.entries[r][c] = self.solution[r][c]