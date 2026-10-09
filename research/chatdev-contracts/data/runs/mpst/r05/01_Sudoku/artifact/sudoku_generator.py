'''
sudoku_generator.py
Responsible for creating new Sudoku puzzles.
A complete, valid 9x9 solution grid is built with a randomized
backtracking algorithm. Cells are then removed one by one; a removal
is only kept when the remaining puzzle still has exactly one solution,
so every generated puzzle is guaranteed to be uniquely solvable.
'''
import random
class SudokuGenerator:
    """Generates Sudoku puzzles (with solutions) for the game."""
    GRID_SIZE = 9
    BOX_SIZE = 3
    DIGITS = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    # Difficulty name -> number of cells removed from the full solution
    DIFFICULTY_LEVELS = {
        "Easy": 36,
        "Medium": 45,
        "Hard": 52,
    }
    def __init__(self, difficulty="Medium"):
        if difficulty not in self.DIFFICULTY_LEVELS:
            raise ValueError(
                "Unknown difficulty '%s'. Choose from: %s"
                % (difficulty, ", ".join(self.DIFFICULTY_LEVELS))
            )
        self.difficulty = difficulty
        self.solution = None   # 9x9 list of lists with the full solution
        self.puzzle = None     # 9x9 list of lists with 0 for empty cells
    def generate(self):
        """Create a new puzzle.
        Returns:
            tuple: (puzzle, solution) as 9x9 lists of lists,
                   empty cells are represented by 0.
        """
        self.solution = self._build_full_grid()
        cells_to_remove = self.DIFFICULTY_LEVELS[self.difficulty]
        self.puzzle = self._carve_puzzle([row[:] for row in self.solution],
                                         cells_to_remove)
        return self.puzzle, self.solution
    # ------------------------------------------------------------------
    # Solution construction
    # ------------------------------------------------------------------
    def _build_full_grid(self):
        """Build a completely filled, valid Sudoku grid."""
        grid = [[0] * self.GRID_SIZE for _ in range(self.GRID_SIZE)]
        self._fill_backtracking(grid, 0)
        return grid
    def _fill_backtracking(self, grid, index):
        """Recursively fill `grid` starting at cell `index` (0..80)."""
        if index == self.GRID_SIZE * self.GRID_SIZE:
            return True
        row, col = divmod(index, self.GRID_SIZE)
        digits = list(self.DIGITS)
        random.shuffle(digits)
        for digit in digits:
            if self._is_safe(grid, row, col, digit):
                grid[row][col] = digit
                if self._fill_backtracking(grid, index + 1):
                    return True
                grid[row][col] = 0
        return False
    def _is_safe(self, grid, row, col, digit):
        """Check that `digit` can be placed at (row, col) without conflict."""
        # Row check
        if digit in grid[row]:
            return False
        # Column check
        if any(grid[r][col] == digit for r in range(self.GRID_SIZE)):
            return False
        # 3x3 box check
        box_row = (row // self.BOX_SIZE) * self.BOX_SIZE
        box_col = (col // self.BOX_SIZE) * self.BOX_SIZE
        for r in range(box_row, box_row + self.BOX_SIZE):
            for c in range(box_col, box_col + self.BOX_SIZE):
                if grid[r][c] == digit:
                    return False
        return True
    # ------------------------------------------------------------------
    # Puzzle carving
    # ------------------------------------------------------------------
    def _carve_puzzle(self, grid, cells_to_remove):
        """Remove cells while keeping the puzzle uniquely solvable."""
        positions = list(range(self.GRID_SIZE * self.GRID_SIZE))
        random.shuffle(positions)
        removed = 0
        for position in positions:
            if removed >= cells_to_remove:
                break
            row, col = divmod(position, self.GRID_SIZE)
            backup = grid[row][col]
            grid[row][col] = 0
            if self._count_solutions(grid, limit=2) == 1:
                removed += 1
            else:
                grid[row][col] = backup  # removal breaks uniqueness -> undo
        return grid
    def _count_solutions(self, grid, limit=2):
        """Count solutions of `grid`, stopping as soon as `limit` is reached."""
        counter = {"count": 0}
        def solve():
            if counter["count"] >= limit:
                return
            target = self._find_empty(grid)
            if target is None:
                counter["count"] += 1
                return
            row, col = target
            for digit in self.DIGITS:
                if self._is_safe(grid, row, col, digit):
                    grid[row][col] = digit
                    solve()
                    grid[row][col] = 0
                    if counter["count"] >= limit:
                        return
        solve()
        return counter["count"]
    def _find_empty(self, grid):
        """Return (row, col) of the first empty cell, or None if full."""
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if grid[row][col] == 0:
                    return (row, col)
        return None