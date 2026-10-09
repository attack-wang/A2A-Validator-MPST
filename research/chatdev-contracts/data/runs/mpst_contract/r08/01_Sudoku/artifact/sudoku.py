"""Core Sudoku logic: puzzle generation, rule validation, mistake checking."""

import random


class SudokuBoard:
    """A 9x9 Sudoku board with unique-solution puzzle generation."""

    def __init__(self, blanks=45, seed=None):
        self.rng = random.Random(seed)
        self.grid = [[0] * 9 for _ in range(9)]
        self.solution = [[0] * 9 for _ in range(9)]
        self.given = [[False] * 9 for _ in range(9)]
        self._generate(blanks)

    # ---------- generation ----------
    def _generate(self, blanks):
        self._fill(0)
        self.solution = [row[:] for row in self.grid]
        cells = [(r, c) for r in range(9) for c in range(9)]
        self.rng.shuffle(cells)
        removed = 0
        for r, c in cells:
            if removed >= blanks:
                break
            backup = self.grid[r][c]
            self.grid[r][c] = 0
            if self._count_solutions(0, 2) != 1:
                self.grid[r][c] = backup
            else:
                removed += 1
        self.given = [[self.grid[r][c] != 0 for c in range(9)] for r in range(9)]

    def _fill(self, idx):
        if idx == 81:
            return True
        r, c = divmod(idx, 9)
        nums = list(range(1, 10))
        self.rng.shuffle(nums)
        for n in nums:
            if self._is_rule_valid(r, c, n):
                self.grid[r][c] = n
                if self._fill(idx + 1):
                    return True
                self.grid[r][c] = 0
        return False

    def _count_solutions(self, idx, limit):
        if idx == 81:
            return 1
        r, c = divmod(idx, 9)
        if self.grid[r][c]:
            return self._count_solutions(idx + 1, limit)
        total = 0
        for n in range(1, 10):
            if self._is_rule_valid(r, c, n):
                self.grid[r][c] = n
                total += self._count_solutions(idx + 1, limit)
                self.grid[r][c] = 0
                if total >= limit:
                    break
        return total

    # ---------- rules ----------
    def _is_rule_valid(self, r, c, n):
        if n == 0:
            return True
        for i in range(9):
            if i != c and self.grid[r][i] == n:
                return False
            if i != r and self.grid[i][c] == n:
                return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if (i, j) != (r, c) and self.grid[i][j] == n:
                    return False
        return True

    # ---------- player actions ----------
    def place(self, r, c, value):
        """Set cell (r, c) to value (1-9); 0 clears. Returns False for given cells."""
        if not (0 <= r < 9 and 0 <= c < 9):
            raise ValueError("Row and column must be between 1 and 9.")
        if not (0 <= value <= 9):
            raise ValueError("Value must be 0-9 (0 clears the cell).")
        if self.given[r][c]:
            return False
        self.grid[r][c] = value
        return True

    def conflicts(self):
        """Cells whose current value duplicates another in its row/column/box."""
        return sorted(
            (r, c) for r in range(9) for c in range(9)
            if self.grid[r][c] and not self._is_rule_valid(r, c, self.grid[r][c])
        )

    def wrong_vs_solution(self):
        """Player-entered cells whose value differs from the unique solution."""
        return sorted(
            (r, c) for r in range(9) for c in range(9)
            if not self.given[r][c] and self.grid[r][c]
            and self.grid[r][c] != self.solution[r][c]
        )

    def is_complete(self):
        """True when every row, column and 3x3 box holds digits 1-9 exactly once."""
        if any(0 in row for row in self.grid):
            return False
        target = set(range(1, 10))
        for i in range(9):
            if set(self.grid[i]) != target:
                return False
            if {self.grid[r][i] for r in range(9)} != target:
                return False
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                box = {self.grid[r][c]
                       for r in range(br, br + 3) for c in range(bc, bc + 3)}
                if box != target:
                    return False
        return True

    def reveal(self):
        self.grid = [row[:] for row in self.solution]
        self.given = [[True] * 9 for _ in range(9)]