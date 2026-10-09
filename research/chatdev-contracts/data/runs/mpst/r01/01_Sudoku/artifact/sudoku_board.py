'''
sudoku_board.py
Core Sudoku game logic module.
This module contains the SudokuBoard class, which is responsible for:
- Storing the 9x9 board state (puzzle clues and player-entered values)
- Generating new random puzzles with a unique solution
- Validating moves according to classic Sudoku rules
- Detecting mistakes (rule conflicts) in the current board
- Detecting when the puzzle has been correctly completed
'''
import random
class SudokuBoard:
    """Represents a 9x9 Sudoku board with puzzle generation and validation logic."""
    SIZE = 9
    BOX_SIZE = 3
    EMPTY = 0
    def __init__(self):
        """Initialize the board with an empty grid and no fixed clues."""
        self.grid = [[self.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.solution = [[self.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.fixed = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]
    # ------------------------------------------------------------------
    # Puzzle generation
    # ------------------------------------------------------------------
    def generate_puzzle(self, difficulty="medium"):
        """Generate a new random puzzle with a unique solution."""
        # difficulty maps to number of cells removed
        removals = {"easy": 35, "medium": 45, "hard": 52}
        cells_to_remove = removals.get(difficulty, 45)
        # Start from a fresh empty board
        self.grid = [[self.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.fixed = [[False for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        # Generate a complete valid board
        self._fill_board(0, 0)
        self.solution = [row[:] for row in self.grid]
        # Remove cells while keeping a unique solution
        self._remove_cells(cells_to_remove)
        # Mark remaining cells as fixed clues
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.grid[r][c] != self.EMPTY:
                    self.fixed[r][c] = True
    def _fill_board(self, row, col):
        """Recursively fill the board completely using randomized backtracking."""
        if row == self.SIZE:
            return True
        next_row, next_col = (row, col + 1) if col < self.SIZE - 1 else (row + 1, 0)
        numbers = list(range(1, self.SIZE + 1))
        random.shuffle(numbers)
        for num in numbers:
            if self.is_valid_placement(row, col, num):
                self.grid[row][col] = num
                if self._fill_board(next_row, next_col):
                    return True
                self.grid[row][col] = self.EMPTY
        return False
    def _remove_cells(self, count):
        """Remove up to `count` cells while preserving a unique solution."""
        cells = [(r, c) for r in range(self.SIZE) for c in range(self.SIZE)]
        random.shuffle(cells)
        removed = 0
        for r, c in cells:
            if removed >= count:
                break
            backup = self.grid[r][c]
            self.grid[r][c] = self.EMPTY
            if self._count_solutions(0, 0, limit=2) != 1:
                self.grid[r][c] = backup  # restore to keep uniqueness
            else:
                removed += 1
    def _count_solutions(self, row, col, limit=2):
        """Count solutions up to `limit` using backtracking."""
        if row == self.SIZE:
            return 1
        next_row, next_col = (row, col + 1) if col < self.SIZE - 1 else (row + 1, 0)
        if self.grid[row][col] != self.EMPTY:
            return self._count_solutions(next_row, next_col, limit)
        total = 0
        for num in range(1, self.SIZE + 1):
            if self.is_valid_placement(row, col, num):
                self.grid[row][col] = num
                total += self._count_solutions(next_row, next_col, limit)
                self.grid[row][col] = self.EMPTY
                if total >= limit:
                    break
        return total
    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def is_valid_placement(self, row, col, value):
        """Check whether `value` can be placed at (row, col) without conflicts."""
        # Row check
        for c in range(self.SIZE):
            if c != col and self.grid[row][c] == value:
                return False
        # Column check
        for r in range(self.SIZE):
            if r != row and self.grid[r][col] == value:
                return False
        # 3x3 box check
        box_row, box_col = (row // self.BOX_SIZE) * self.BOX_SIZE, (col // self.BOX_SIZE) * self.BOX_SIZE
        for r in range(box_row, box_row + self.BOX_SIZE):
            for c in range(box_col, box_col + self.BOX_SIZE):
                if (r, c) != (row, col) and self.grid[r][c] == value:
                    return False
        return True
    def find_conflicts(self):
        """Return a set of (row, col) positions that conflict with Sudoku rules."""
        conflicts = set()
        # rows
        for r in range(self.SIZE):
            seen = {}
            for c in range(self.SIZE):
                v = self.grid[r][c]
                if v != self.EMPTY:
                    if v in seen:
                        conflicts.add((r, seen[v]))
                        conflicts.add((r, c))
                    else:
                        seen[v] = c
        # columns
        for c in range(self.SIZE):
            seen = {}
            for r in range(self.SIZE):
                v = self.grid[r][c]
                if v != self.EMPTY:
                    if v in seen:
                        conflicts.add((seen[v], c))
                        conflicts.add((r, c))
                    else:
                        seen[v] = r
        # boxes
        for box_r in range(0, self.SIZE, self.BOX_SIZE):
            for box_c in range(0, self.SIZE, self.BOX_SIZE):
                seen = {}
                for r in range(box_r, box_r + self.BOX_SIZE):
                    for c in range(box_c, box_c + self.BOX_SIZE):
                        v = self.grid[r][c]
                        if v != self.EMPTY:
                            if v in seen:
                                conflicts.add(seen[v])
                                conflicts.add((r, c))
                            else:
                                seen[v] = (r, c)
        return conflicts
    def is_complete(self):
        """Check whether the board is completely and correctly filled."""
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if self.grid[r][c] == self.EMPTY:
                    return False
        return len(self.find_conflicts()) == 0
    # ------------------------------------------------------------------
    # Board manipulation
    # ------------------------------------------------------------------
    def set_value(self, row, col, value):
        """Set a player-entered value at (row, col). Returns True on success."""
        if self.fixed[row][col]:
            return False
        if value == self.EMPTY:
            self.grid[row][col] = self.EMPTY
            return True
        if 1 <= value <= self.SIZE:
            self.grid[row][col] = value
            return True
        return False
    def get_value(self, row, col):
        """Return the current value at (row, col)."""
        return self.grid[row][col]
    def is_fixed(self, row, col):
        """Return True if (row, col) holds a fixed puzzle clue."""
        return self.fixed[row][col]
    def get_solution_value(self, row, col):
        """Return the solution value for (row, col) (used by the hint feature)."""
        return self.solution[row][col]