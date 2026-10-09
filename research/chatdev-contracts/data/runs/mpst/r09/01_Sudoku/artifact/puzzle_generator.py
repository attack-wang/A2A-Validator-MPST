'''
puzzle_generator.py
Defines the PuzzleGenerator class, responsible for creating new Sudoku
puzzles. It first generates a complete, valid solution using randomized
backtracking, then removes cells while guaranteeing that the puzzle keeps
a unique solution. Difficulty levels control how many cells are removed.
'''
import random
class PuzzleGenerator:
    """Generates Sudoku puzzles with unique solutions at various difficulties."""
    SIZE = 9
    BOX_SIZE = 3
    EMPTY = 0
    DIFFICULTY_TARGETS = {
        "Easy": 40,
        "Medium": 48,
        "Hard": 54,
    }
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    def generate_puzzle(self, difficulty="Medium"):
        """Generate a new puzzle.
        Returns (puzzle_grid, solution_grid, given_mask).
        """
        target = self.DIFFICULTY_TARGETS.get(difficulty, self.DIFFICULTY_TARGETS["Medium"])
        solution = self._generate_full_solution()
        puzzle = [row[:] for row in solution]
        self._carve_puzzle(puzzle, target)
        given = [[puzzle[r][c] != self.EMPTY for c in range(self.SIZE)] for r in range(self.SIZE)]
        return puzzle, solution, given
    def _generate_full_solution(self):
        """Build a complete valid grid via randomized backtracking."""
        board = [[self.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self._backtrack(board)
        return board
    def _backtrack(self, board):
        """Fill board in place; return True when fully solved."""
        cell = self._find_best_cell(board)
        if cell is None:
            return True
        r, c = cell
        digits = list(range(1, 10))
        self.rng.shuffle(digits)
        for d in digits:
            if self._is_safe(board, r, c, d):
                board[r][c] = d
                if self._backtrack(board):
                    return True
                board[r][c] = self.EMPTY
        return False
    def _find_best_cell(self, board):
        """Return the empty cell with the fewest legal candidates (MRV)."""
        best = None
        best_count = None
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if board[r][c] == self.EMPTY:
                    count = sum(1 for d in range(1, 10) if self._is_safe(board, r, c, d))
                    if count == 0:
                        return (r, c)  # dead end; fail fast
                    if best is None or count < best_count:
                        best = (r, c)
                        best_count = count
                        if count == 1:
                            return best
        return best
    def _is_safe(self, board, row, col, value):
        """Return True if value can be placed at (row, col) without conflict."""
        if any(board[row][c] == value for c in range(self.SIZE)):
            return False
        if any(board[r][col] == value for r in range(self.SIZE)):
            return False
        br = (row // self.BOX_SIZE) * self.BOX_SIZE
        bc = (col // self.BOX_SIZE) * self.BOX_SIZE
        return all(board[r][c] != value
                   for r in range(br, br + self.BOX_SIZE)
                   for c in range(bc, bc + self.BOX_SIZE))
    def _carve_puzzle(self, puzzle, target):
        """Remove up to `target` cells while keeping the solution unique."""
        removed = 0
        cells = [(r, c) for r in range(self.SIZE) for c in range(self.SIZE)]
        self.rng.shuffle(cells)
        for r, c in cells:
            if removed >= target:
                break
            backup = puzzle[r][c]
            puzzle[r][c] = self.EMPTY
            if self._count_solutions([row[:] for row in puzzle], limit=2) != 1:
                puzzle[r][c] = backup  # restore: removal broke uniqueness
            else:
                removed += 1
        return removed
    def _count_solutions(self, board, limit=2):
        """Count solutions up to `limit` with early exit."""
        count = 0
        def solve():
            nonlocal count
            cell = self._find_best_cell(board)
            if cell is None:
                count += 1
                return count >= limit
            r, c = cell
            for d in range(1, 10):
                if self._is_safe(board, r, c, d):
                    board[r][c] = d
                    stop = solve()
                    board[r][c] = self.EMPTY
                    if stop:
                        return True
            return False
        solve()
        return count