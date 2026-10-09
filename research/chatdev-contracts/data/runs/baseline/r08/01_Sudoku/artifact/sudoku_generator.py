'''
sudoku_generator.py
Generates random Sudoku puzzles. A complete solved grid is produced with
a randomized backtracking solver, then cells are removed one by one while
verifying (with a solution counter) that the puzzle keeps a unique
solution. Difficulty levels control how many cells are removed.
'''
import random
class SudokuGenerator:
    """Creates random Sudoku puzzles with unique solutions."""
    SIZE = 9
    BOX_SIZE = 3
    # Number of cells removed per difficulty level (81 - removed = clues).
    DIFFICULTY_LEVELS = {
        "easy": 40,      # ~41 clues
        "medium": 50,    # ~31 clues
        "hard": 56,      # ~25 clues
    }
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    def generate_puzzle(self, difficulty="medium"):
        """Return (puzzle, solution) grids for the requested difficulty."""
        if difficulty not in self.DIFFICULTY_LEVELS:
            difficulty = "medium"
        solution = self.generate_full_grid()
        puzzle = [row[:] for row in solution]
        target = self.DIFFICULTY_LEVELS[difficulty]
        self._remove_cells(puzzle, target)
        return puzzle, solution
    def generate_full_grid(self):
        grid = [[0] * self.SIZE for _ in range(self.SIZE)]
        self._fill_grid(grid)
        return grid
    def _fill_grid(self, grid):
        """Fill the grid completely using randomized backtracking."""
        for row, col in self._empty_cells_ordered(grid):
            candidates = list(range(1, 10))
            self.rng.shuffle(candidates)
            for value in candidates:
                if self._is_safe(grid, row, col, value):
                    grid[row][col] = value
                    if self._fill_grid(grid):
                        return True
                    grid[row][col] = 0
            return False
        return True
    def _empty_cells_ordered(self, grid):
        cells = [(r, c) for r in range(self.SIZE) for c in range(self.SIZE) if grid[r][c] == 0]
        # Use a fixed scan order for determinism of the recursion; randomization
        # comes from shuffling candidate digits.
        return cells
    def _is_safe(self, grid, row, col, value):
        # row
        if any(grid[row][c] == value for c in range(self.SIZE)):
            return False
        # column
        if any(grid[r][col] == value for r in range(self.SIZE)):
            return False
        # box
        br, bc = (row // self.BOX_SIZE) * self.BOX_SIZE, (col // self.BOX_SIZE) * self.BOX_SIZE
        for r in range(br, br + self.BOX_SIZE):
            for c in range(bc, bc + self.BOX_SIZE):
                if grid[r][c] == value:
                    return False
        return True
    def _remove_cells(self, puzzle, target_removed):
        """Remove up to `target_removed` cells while keeping a unique solution."""
        cells = [(r, c) for r in range(self.SIZE) for c in range(self.SIZE)]
        self.rng.shuffle(cells)
        removed = 0
        for row, col in cells:
            if removed >= target_removed:
                break
            backup = puzzle[row][col]
            puzzle[row][col] = 0
            if self._count_solutions(puzzle, limit=2) != 1:
                puzzle[row][col] = backup  # restore to keep uniqueness
            else:
                removed += 1
        return removed
    def _count_solutions(self, grid, limit=2):
        """Count solutions of `grid`, stopping as soon as `limit` is reached."""
        grid_copy = [row[:] for row in grid]
        return self._count_solutions_rec(grid_copy, limit)
    def _count_solutions_rec(self, grid, limit):
        best = None
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if grid[r][c] == 0:
                    best = (r, c)
                    break
            if best:
                break
        if best is None:
            return 1
        row, col = best
        total = 0
        for value in range(1, 10):
            if self._is_safe(grid, row, col, value):
                grid[row][col] = value
                total += self._count_solutions_rec(grid, limit)
                grid[row][col] = 0
                if total >= limit:
                    break
        return total