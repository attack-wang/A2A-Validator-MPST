'''
sudoku_board.py
Defines the SudokuBoard class: the pure rules/data model of the 9x9 Sudoku
puzzle. It stores the grid, tracks which cells are fixed clues, validates
placements, detects rule conflicts (row/column/3x3 subgrid duplicates) and
decides whether the puzzle is complete and correct.
'''
from collections import deque
class SudokuBoard:
    """Pure data model of a 9x9 Sudoku board (rules only, no I/O)."""
    SIZE = 9
    EMPTY = 0
    BOX = 3
    def __init__(self, puzzle=None):
        self.grid = [[self.EMPTY] * self.SIZE for _ in range(self.SIZE)]
        self.fixed = [[False] * self.SIZE for _ in range(self.SIZE)]
        if puzzle:
            self.load_puzzle(puzzle)
    # ------------------------------------------------------------------ #
    # board setup
    # ------------------------------------------------------------------ #
    def load_puzzle(self, puzzle):
        """Replace the whole grid; every non-zero cell becomes a fixed clue."""
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                self.grid[r][c] = puzzle[r][c]
                self.fixed[r][c] = puzzle[r][c] != self.EMPTY
    # ------------------------------------------------------------------ #
    # cell access
    # ------------------------------------------------------------------ #
    def get_cell(self, row, col):
        return self.grid[row][col]
    def set_cell(self, row, col, value):
        """
        Store a digit (0-9) in an editable cell. Fixed clues are protected.
        Returns True when the grid was modified, False otherwise.
        """
        if not self._in_bounds(row, col):
            return False
        if not self._valid_value(value):
            return False
        if self.fixed[row][col]:
            return False
        if self.grid[row][col] == value:
            return False
        self.grid[row][col] = value
        return True
    def clear_cell(self, row, col):
        """Erase one editable cell. Returns True when something was erased."""
        if not self._in_bounds(row, col):
            return False
        if self.fixed[row][col]:
            return False
        if self.grid[row][col] == self.EMPTY:
            return False
        self.grid[row][col] = self.EMPTY
        return True
    def clear_all_player_entries(self):
        """Erase every non-fixed cell (clues are kept)."""
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if not self.fixed[r][c]:
                    self.grid[r][c] = self.EMPTY
    def is_fixed(self, row, col):
        return self.fixed[row][col]
    # ------------------------------------------------------------------ #
    # rules
    # ------------------------------------------------------------------ #
    def is_valid_placement(self, row, col, value):
        """Would placing value at (row, col) break row/column/box rules?"""
        if not self._in_bounds(row, col) or not self._valid_value(value):
            return False
        for c in range(self.SIZE):
            if c != col and self.grid[row][c] == value:
                return False
        for r in range(self.SIZE):
            if r != row and self.grid[r][col] == value:
                return False
        box_row, box_col = self.BOX * (row // self.BOX), self.BOX * (col // self.BOX)
        for r in range(box_row, box_row + self.BOX):
            for c in range(box_col, box_col + self.BOX):
                if (r, c) != (row, col) and self.grid[r][c] == value:
                    return False
        return True
    def find_conflicts(self):
        """Set of (row, col) cells that duplicate a value in their unit."""
        conflicts = set()
        units = []
        # rows
        for r in range(self.SIZE):
            units.append([(r, c) for c in range(self.SIZE)])
        # columns
        for c in range(self.SIZE):
            units.append([(r, c) for r in range(self.SIZE)])
        # 3x3 boxes
        for box_row in range(0, self.SIZE, self.BOX):
            for box_col in range(0, self.SIZE, self.BOX):
                units.append([
                    (r, c)
                    for r in range(box_row, box_row + self.BOX)
                    for c in range(box_col, box_col + self.BOX)
                ])
        for unit in units:
            self._scan(unit, conflicts)
        return conflicts
    def _scan(self, cells, conflicts):
        """Mark every duplicate value inside one row/column/box unit."""
        seen = {}
        for pos, value in cells:
            v = self.grid[pos[0]][pos[1]]
            if v == self.EMPTY:
                continue
            if v in seen:
                conflicts.add(pos)
                conflicts.add(seen[v])
            else:
                seen[v] = pos
    def is_complete(self):
        """True when all 81 cells are filled and no rule is violated."""
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.grid[r][c] == self.EMPTY:
                    return False
        return not self.find_conflicts()
    def is_correct(self, solution):
        """True when the grid matches the given solution exactly."""
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.grid[r][c] != solution[r][c]:
                    return False
        return True
    # ------------------------------------------------------------------ #
    # helpers
    # ------------------------------------------------------------------ #
    def _in_bounds(self, row, col):
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE
    def _valid_value(self, value):
        return isinstance(value, int) and self.EMPTY <= value <= 9