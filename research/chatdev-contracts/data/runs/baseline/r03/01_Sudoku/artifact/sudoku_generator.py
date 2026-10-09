'''
sudoku_generator.py
Generates Sudoku puzzles and their solutions.
A complete, valid 9x9 board is produced with a randomized backtracking
search, then cells are removed one at a time while a solution counter
guarantees the resulting puzzle keeps a unique solution. Difficulty
controls how many cells are removed.
'''
import random
class SudokuGenerator:
    """Generates Sudoku puzzles with unique solutions at various difficulties."""
    EMPTY = 0
    SIZE = 9
    BOX = 3
    # Approximate number of cells removed per difficulty level.
    DIFFICULTY_LEVELS = {
        "easy": 35,
        "medium": 45,
        "hard": 52,
    }
    def __init__(self, seed=None):
        self._rng = random.Random(seed)
    def generate(self, difficulty="medium"):
        """Return (puzzle, solution) tuple for the requested difficulty."""
        solution = self._generate_full_board()
        puzzle = [row[:] for row in solution]
        target = self.DIFFICULTY_LEVELS.get(difficulty, self.DIFFICULTY_LEVELS["medium"])
        self._remove_cells(puzzle, target)
        return puzzle, solution
    def _generate_full_board(self):
        board = [[self.EMPTY] * self.SIZE for _ in range(self.SIZE)]
        self._fill_board(board)
        return board
    def _fill_board(self, board):
        """Fill board completely using backtracking with shuffled candidates."""
        for row, col in self._empty_cells(board):
            candidates = [n for n in range(1, 10)]
            self._rng.shuffle(candidates)
            for value in candidates:
                if self._is_safe(board, row, col, value):
                    board[row][col] = value
                    if self._fill_board(board):
                        return True
                    board[row][col] = self.EMPTY
            return False
        return True
    def _empty_cells(self, board):
        cells = [(r, c) for r in range(self.SIZE) for c in range(self.SIZE) if board[r][c] == self.EMPTY]
        # Process in a fixed order; randomness comes from candidate shuffling.
        return cells
    def _is_safe(self, board, row, col, value):
        # Row and column
        for i in range(self.SIZE):
            if board[row][i] == value or board[i][col] == value:
                return False
        # 3x3 box
        box_row, box_col = (row // self.BOX) * self.BOX, (col // self.BOX) * self.BOX
        for r in range(box_row, box_row + self.BOX):
            for c in range(box_col, box_col + self.BOX):
                if board[r][c] == value:
                    return False
        return True
    def _remove_cells(self, puzzle, target_empty):
        """Remove cells while keeping the puzzle's solution unique."""
        cells = [(r, c) for r in range(self.SIZE) for c in range(self.SIZE)]
        self._rng.shuffle(cells)
        removed = 0
        for row, col in cells:
            if removed >= target_empty:
                break
            backup = puzzle[row][col]
            puzzle[row][col] = self.EMPTY
            if self._count_solutions(puzzle, limit=2) != 1:
                puzzle[row][col] = backup  # restore to keep uniqueness
            else:
                removed += 1
        return removed
    def _count_solutions(self, board, limit=2):
        """Count solutions up to `limit` using backtracking."""
        def solve():
            # find first empty cell
            for r in range(self.SIZE):
                for c in range(self.SIZE):
                    if board[r][c] == self.EMPTY:
                        count = 0
                        for value in range(1, 10):
                            if self._is_safe(board, r, c, value):
                                board[r][c] = value
                                count += solve()
                                board[r][c] = self.EMPTY
                                if count >= limit:
                                    return count
                        return count
            return 1
        return solve()