'''
sudoku_generator.py
Generates full Sudoku solutions via randomized backtracking and carves
unique-solution puzzles by removing cells while preserving solvability.
Difficulty levels control how many cells are removed.
'''
import random
class SudokuGenerator:
    """Random Sudoku puzzle generator with unique-solution guarantee."""
    SIZE = 9
    BOX = 3
    DIFFICULTY_HOLES = {
        "easy": 36,
        "medium": 46,
        "hard": 52,
        "expert": 56,
    }
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    # ------------------------------------------------------------------
    # Safety / candidate helpers
    # ------------------------------------------------------------------
    def _is_safe(self, board, row, col, value):
        """Check whether value can be placed at (row, col) without conflict."""
        for k in range(self.SIZE):
            if board[row][k] == value or board[k][col] == value:
                return False
        box_row = (row // self.BOX) * self.BOX
        box_col = (col // self.BOX) * self.BOX
        for r in range(box_row, box_row + self.BOX):
            for c in range(box_col, box_col + self.BOX):
                if board[r][c] == value:
                    return False
        return True
    # ------------------------------------------------------------------
    # Full-solution generation (randomized backtracking)
    # ------------------------------------------------------------------
    def _fill_board(self, board):
        """Fill board completely using randomized backtracking."""
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if board[r][c] == 0:
                    values = list(range(1, 10))
                    self.rng.shuffle(values)
                    for value in values:
                        if self._is_safe(board, r, c, value):
                            board[r][c] = value
                            if self._fill_board(board):
                                return True
                            board[r][c] = 0
                    return False
        return True
    def generate_solution(self):
        """Return a complete, valid 9x9 Sudoku solution."""
        board = [[0] * self.SIZE for _ in range(self.SIZE)]
        self._fill_board(board)
        return board
    # ------------------------------------------------------------------
    # Solution counting (used to guarantee puzzle uniqueness)
    # ------------------------------------------------------------------
    def _count_solutions_helper(self, board, limit):
        # Find the empty cell with the fewest candidates for efficiency
        best = None
        best_candidates = None
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if board[r][c] == 0:
                    candidates = [v for v in range(1, 10) if self._is_safe(board, r, c, v)]
                    if best_candidates is None or len(candidates) < len(best_candidates):
                        best = (r, c)
                        best_candidates = candidates
                        if len(candidates) <= 1:
                            break
            else:
                continue
            break
        if best is None:
            return 1  # no empty cells: exactly one complete solution
        if not best_candidates:
            return 0  # dead end
        total = 0
        row, col = best
        for value in best_candidates:
            board[row][col] = value
            total += self._count_solutions_helper(board, limit)
            board[row][col] = 0
            if total >= limit:
                break
        return total
    def _count_solutions(self, board, limit=2):
        """Count solutions up to `limit` (early exit for speed)."""
        work = [row[:] for row in board]
        return self._count_solutions_helper(work, limit)
    # ------------------------------------------------------------------
    # Puzzle carving (hole digging with uniqueness preservation)
    # ------------------------------------------------------------------
    def _remove_cells(self, puzzle, holes):
        cells = [(r, c) for r in range(9) for c in range(9)]
        self.rng.shuffle(cells)
        removed = 0
        for r, c in cells:
            if removed >= holes:
                break
            backup = puzzle[r][c]
            puzzle[r][c] = 0
            if self._count_solutions(puzzle, limit=2) == 1:
                removed += 1
            else:
                puzzle[r][c] = backup
    def generate_puzzle(self, difficulty="medium"):
        """Return (puzzle, solution) with a unique solution for the difficulty."""
        holes = self.DIFFICULTY_HOLES.get(difficulty, self.DIFFICULTY_HOLES["medium"])
        solution = self.generate_solution()
        puzzle = [row[:] for row in solution]
        self._remove_cells(puzzle, holes)
        return puzzle, solution