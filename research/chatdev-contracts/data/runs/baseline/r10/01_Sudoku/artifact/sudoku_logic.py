'''
sudoku_logic.py
Core Sudoku game logic module.
This module contains the SudokuBoard class, which is responsible for:
  * Generating new Sudoku puzzles with guaranteed unique solutions
  * Managing the state of the 9x9 board (given cells vs. player entries)
  * Validating player input against Sudoku rules (row, column, 3x3 subgrid)
  * Detecting mistakes (conflicting cells)
  * Detecting puzzle completion
The module is completely independent of any GUI framework so it can be
unit-tested or reused with other front-ends.
'''
import random
GRID_SIZE = 9
BOX_SIZE = 3
class SudokuBoard:
    """Core logic for a classic 9x9 Sudoku game (puzzle generation, validation,
    mistake detection and completion checking), independent of any GUI."""
    def __init__(self):
        self.solution = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.puzzle = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.given = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    # ------------------------------------------------------------------
    # Puzzle generation
    # ------------------------------------------------------------------
    def generate_puzzle(self, difficulty='medium'):
        """Generate a new puzzle with a unique solution for the given difficulty."""
        self.solution = self._generate_full_grid()
        self.puzzle = [row[:] for row in self.solution]
        removals = {'easy': 35, 'medium': 45, 'hard': 52}.get(difficulty, 45)
        self._remove_cells(removals)
        self.board = [row[:] for row in self.puzzle]
        self.given = [[self.puzzle[r][c] != 0 for c in range(GRID_SIZE)]
                      for r in range(GRID_SIZE)]
    def new_game(self, difficulty='medium'):
        """Alias of generate_puzzle kept for API convenience."""
        self.generate_puzzle(difficulty)
    def _generate_full_grid(self):
        """Generate a complete, valid, randomly-filled Sudoku grid."""
        grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self._fill_grid(grid)
        return grid
    def _fill_grid(self, grid):
        """Fill the grid using randomized backtracking. Returns True on success."""
        empty = self._find_empty(grid)
        if empty is None:
            return True
        row, col = empty
        digits = list(range(1, 10))
        random.shuffle(digits)
        for digit in digits:
            if self._is_valid_placement(grid, row, col, digit):
                grid[row][col] = digit
                if self._fill_grid(grid):
                    return True
                grid[row][col] = 0
        return False
    def _find_empty(self, grid):
        """Return (row, col) of the first empty cell, or None if the grid is full."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if grid[r][c] == 0:
                    return (r, c)
        return None
    def _is_valid_placement(self, grid, row, col, digit):
        """Check whether digit can be placed at (row, col) without conflicts."""
        if digit in grid[row]:
            return False
        for r in range(GRID_SIZE):
            if grid[r][col] == digit:
                return False
        box_row, box_col = (row // BOX_SIZE) * BOX_SIZE, (col // BOX_SIZE) * BOX_SIZE
        for r in range(box_row, box_row + BOX_SIZE):
            for c in range(box_col, box_col + BOX_SIZE):
                if grid[r][c] == digit:
                    return False
        return True
    def _remove_cells(self, count):
        """Remove up to `count` cells while keeping the puzzle uniquely solvable."""
        cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
        random.shuffle(cells)
        removed = 0
        for row, col in cells:
            if removed >= count:
                break
            backup = self.puzzle[row][col]
            if backup == 0:
                continue
            self.puzzle[row][col] = 0
            if self._count_solutions([row[:] for row in self.puzzle], 2) != 1:
                self.puzzle[row][col] = backup  # restore to keep unique solution
            else:
                removed += 1
    def _count_solutions(self, grid, limit):
        """Count solutions of `grid` up to `limit` using backtracking."""
        empty = self._find_empty(grid)
        if empty is None:
            return 1
        row, col = empty
        total = 0
        for digit in range(1, 10):
            if self._is_valid_placement(grid, row, col, digit):
                grid[row][col] = digit
                total += self._count_solutions(grid, limit)
                grid[row][col] = 0
                if total >= limit:
                    break
        return total
    # ------------------------------------------------------------------
    # Board state access / mutation
    # ------------------------------------------------------------------
    def get_cell(self, row, col):
        """Return the current value of the cell at (row, col); 0 means empty."""
        return self.board[row][col]
    def set_cell(self, row, col, value):
        """Set a player value (1-9) or clear (0) a non-given cell. Returns True on success."""
        if self.given[row][col] or not (0 <= value <= 9):
            return False
        self.board[row][col] = value
        return True
    def is_given(self, row, col):
        """Return True if the cell at (row, col) is a pre-filled given."""
        return self.given[row][col]
    def clear_user_entries(self):
        """Erase every player-entered value, keeping the original givens."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if not self.given[r][c]:
                    self.board[r][c] = 0
    def reveal_solution(self):
        """Fill the board with the stored solution (used by the Reveal button)."""
        self.board = [row[:] for row in self.solution]
    def get_hint(self):
        """Reveal one correct value on a wrong/empty player cell.
        Returns (row, col, value) or None when nothing left to hint.
        """
        candidates = []
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if not self.given[r][c] and self.board[r][c] != self.solution[r][c]:
                    candidates.append((r, c))
        if not candidates:
            return None
        row, col = random.choice(candidates)
        self.board[row][col] = self.solution[row][col]
        return (row, col, self.solution[row][col])
    # ------------------------------------------------------------------
    # Validation / mistake / completion detection
    # ------------------------------------------------------------------
    def find_conflicts(self):
        """Return the set of (row, col) cells that violate row/column/box rules."""
        conflicts = set()
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = self.board[r][c]
                if value == 0:
                    continue
                # row / column peers
                peers = [(r, k) for k in range(GRID_SIZE) if k != c]
                peers += [(k, c) for k in range(GRID_SIZE) if k != r]
                box_row, box_col = (r // BOX_SIZE) * BOX_SIZE, (c // BOX_SIZE) * BOX_SIZE
                peers += [(br, bc)
                          for br in range(box_row, box_row + BOX_SIZE)
                          for bc in range(box_col, box_col + BOX_SIZE)
                          if (br, bc) != (r, c)]
                if any(self.board[pr][pc] == value for pr, pc in peers):
                    conflicts.add((r, c))
        return conflicts
    def find_solution_mismatches(self):
        """Return the set of player cells whose value differs from the solution."""
        return {(r, c)
                for r in range(GRID_SIZE)
                for c in range(GRID_SIZE)
                if not self.given[r][c] and self.board[r][c] != 0
                and self.board[r][c] != self.solution[r][c]}
    def is_complete(self):
        """Return True when every cell is filled and consistent with the solution."""
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c] != self.solution[r][c]:
                    return False
        return True