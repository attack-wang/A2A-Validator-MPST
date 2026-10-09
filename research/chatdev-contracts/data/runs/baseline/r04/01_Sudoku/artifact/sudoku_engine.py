'''
sudoku_engine.py
Core game logic for the classic Sudoku puzzle game (GUI-independent).
This module is the single source of truth for all non-GUI logic and contains:
- SudokuSolver:    backtracking solver/counter used for generating puzzles,
                   verifying uniqueness and revealing solutions.
- SudokuBoard:     the mutable game state (grid + fixed-cell mask) with
                   rule validation, conflict detection and completion checks.
- SudokuGenerator: random puzzle generation with guaranteed unique solutions
                   at three difficulty levels (easy / medium / hard).
'''
import random
class SudokuSolver:
    """Backtracking solver/counter used by the generator and the GUI."""
    @staticmethod
    def _find_empty(grid):
        """Return (row, col) of the first empty cell, or None if full."""
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    return row, col
        return None
    @staticmethod
    def is_safe(grid, row, col, value):
        """Return True if `value` can be placed at (row, col) without
        violating the row, column or 3x3 subgrid rules."""
        if value in grid[row]:
            return False
        for r in range(9):
            if grid[r][col] == value:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if grid[r][c] == value:
                    return False
        return True
    @staticmethod
    def solve(grid):
        """Solve the grid in place; return True if a solution exists."""
        empty = SudokuSolver._find_empty(grid)
        if empty is None:
            return True
        row, col = empty
        for value in range(1, 10):
            if SudokuSolver.is_safe(grid, row, col, value):
                grid[row][col] = value
                if SudokuSolver.solve(grid):
                    return True
                grid[row][col] = 0
        return False
    @staticmethod
    def count_solutions(grid, limit=2):
        """Count solutions of the grid, stopping once `limit` is reached."""
        return SudokuSolver._count(grid, limit)
    @staticmethod
    def _count(grid, limit):
        """Recursive solution counter with an early stop at `limit`."""
        empty = SudokuSolver._find_empty(grid)
        if empty is None:
            return 1
        row, col = empty
        total = 0
        for value in range(1, 10):
            if SudokuSolver.is_safe(grid, row, col, value):
                grid[row][col] = value
                total += SudokuSolver._count(grid, limit)
                grid[row][col] = 0
                if total >= limit:
                    break
        return total
class SudokuBoard:
    """Mutable state of a Sudoku game: the 9x9 grid, which cells are
    fixed clues, rule validation, conflict detection and completion tests."""
    SIZE = 9
    def __init__(self, puzzle=None, solution=None):
        """Create a board from an optional 9x9 `puzzle` (0 = empty cell)
        and an optional known `solution`."""
        if puzzle is None:
            puzzle = [[0] * self.SIZE for _ in range(self.SIZE)]
        self.grid = [list(row) for row in puzzle]
        self.solution = [list(row) for row in solution] if solution else None
        self.fixed = [[self.grid[r][c] != 0 for c in range(self.SIZE)]
                      for r in range(self.SIZE)]
    def in_bounds(self, row, col):
        """True if (row, col) lies inside the 9x9 board."""
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE
    def get_cell(self, row, col):
        """Return the current value (0 = empty) of the cell."""
        return self.grid[row][col]
    def is_fixed(self, row, col):
        """True if the cell holds an immutable puzzle clue."""
        return self.fixed[row][col]
    def set_cell(self, row, col, value):
        """Place `value` (1-9) in an editable cell; 0 clears it.
        Returns True if the board was modified."""
        if self.fixed[row][col]:
            return False
        if value not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
            return False
        self.grid[row][col] = value
        return True
    def clear_cell(self, row, col):
        """Clear an editable cell (fixed clues are protected)."""
        return self.set_cell(row, col, 0)
    def clear_user_entries(self):
        """Reset every editable cell to empty (fixed clues are kept)."""
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if not self.fixed[r][c]:
                    self.grid[r][c] = 0
    def is_valid_placement(self, row, col, value):
        """True if `value` may be placed at (row, col) without breaking
        the row/column/subgrid rules (the cell's own current value is
        ignored during the check)."""
        if value == 0:
            return True
        for c in range(self.SIZE):
            if c != col and self.grid[row][c] == value:
                return False
        for r in range(self.SIZE):
            if r != row and self.grid[r][col] == value:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r != row or c != col) and self.grid[r][c] == value:
                    return False
        return True
    def find_conflicts(self):
        """Return a set of (row, col) tuples for every cell that shares
        a duplicate value within its row, column or 3x3 subgrid."""
        conflicts = set()
        for unit in self._all_units():
            positions = {}
            for (r, c) in unit:
                value = self.grid[r][c]
                if value != 0:
                    positions.setdefault(value, []).append((r, c))
            for cells in positions.values():
                if len(cells) > 1:
                    conflicts.update(cells)
        return conflicts
    def _all_units(self):
        """Return all 27 units (9 rows, 9 columns, 9 subgrids)."""
        units = []
        for r in range(self.SIZE):  # rows
            units.append([(r, c) for c in range(self.SIZE)])
        for c in range(self.SIZE):  # columns
            units.append([(r, c) for r in range(self.SIZE)])
        for br in range(0, self.SIZE, 3):  # 3x3 subgrids
            for bc in range(0, self.SIZE, 3):
                units.append([(br + i, bc + j)
                              for i in range(3) for j in range(3)])
        return units
    def is_complete(self):
        """True when every cell contains a digit from 1 to 9."""
        return all(self.grid[r][c] != 0
                   for r in range(self.SIZE) for c in range(self.SIZE))
    def is_solved(self):
        """True when the board is completely filled and contains no
        rule violations (i.e. it is a valid solution)."""
        return self.is_complete() and not self.find_conflicts()
    def count_filled(self):
        """Number of non-empty cells."""
        return sum(1 for r in range(self.SIZE) for c in range(self.SIZE)
                   if self.grid[r][c] != 0)
    def count_empty(self):
        """Number of empty cells."""
        return self.SIZE * self.SIZE - self.count_filled()
class SudokuGenerator:
    """Generates random Sudoku puzzles with a guaranteed unique solution."""
    DIFFICULTY_CLUES = {"easy": 40, "medium": 34, "hard": 28}
    def generate(self, difficulty="medium"):
        """Return (puzzle, solution) — the exact 2-tuple the GUI unpacks.
        `puzzle` is a 9x9 list of lists with 0 for empty cells."""
        target = self.DIFFICULTY_CLUES.get(difficulty, 34)
        solution = [[0] * 9 for _ in range(9)]
        self._fill_board(solution)
        puzzle = [row[:] for row in solution]
        self._remove_cells(puzzle, target)
        return puzzle, solution
    def _fill_board(self, grid):
        """Fill `grid` completely with a random valid solution
        (randomized backtracking)."""
        empty = SudokuSolver._find_empty(grid)
        if empty is None:
            return True
        row, col = empty
        values = list(range(1, 10))
        random.shuffle(values)
        for value in values:
            if SudokuSolver.is_safe(grid, row, col, value):
                grid[row][col] = value
                if self._fill_board(grid):
                    return True
                grid[row][col] = 0
        return False
    def _remove_cells(self, grid, target_clues):
        """Remove cells from a full solution while keeping the puzzle's
        solution unique, until `target_clues` remain (or no further cell
        can be removed without breaking uniqueness)."""
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        clues = 81
        for (r, c) in cells:
            if clues <= target_clues:
                break
            removed = grid[r][c]
            grid[r][c] = 0
            test_grid = [row[:] for row in grid]
            if SudokuSolver.count_solutions(test_grid, limit=2) == 1:
                clues -= 1
            else:
                grid[r][c] = removed
        return clues