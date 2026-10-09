'''
sudoku_generator.py
Generates random Sudoku puzzles. It first builds a complete valid board
using randomized backtracking, then removes cells while guaranteeing the
puzzle keeps a unique solution. Difficulty controls how many cells are
removed. A retry cap prevents long searches for very sparse puzzles.
'''
import random
from sudoku_solver import SudokuSolver
class SudokuGenerator:
    """Creates random, uniquely-solvable Sudoku puzzles."""
    SIZE = 9
    BOX_SIZE = 3
    MAX_ATTEMPTS = 30
    DIFFICULTY_HOLES = {
        "easy": 35,
        "medium": 45,
        "hard": 52,
    }
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    def generate_full_board(self):
        board = [[0] * self.SIZE for _ in range(self.SIZE)]
        self._fill_board(board)
        return board
    def _fill_board(self, board):
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                if board[r][c] != 0:
                    continue
                digits = list(range(1, 10))
                self.rng.shuffle(digits)
                for value in digits:
                    if SudokuSolver.is_safe(board, r, c, value):
                        board[r][c] = value
                        if self._fill_board(board):
                            return True
                        board[r][c] = 0
                return False
        return True
    def generate_puzzle(self, difficulty="medium"):
        holes = self.DIFFICULTY_HOLES.get(difficulty, self.DIFFICULTY_HOLES["medium"])
        for attempt in range(self.MAX_ATTEMPTS):
            solution = self.generate_full_board()
            puzzle = [row[:] for row in solution]
            if self._dig_holes(puzzle, holes):
                return puzzle, solution
        # Fallback: return the last generated puzzle even if the hole target
        # was not fully reached, so the caller always receives a valid game.
        return puzzle, solution
    def _dig_holes(self, puzzle, holes):
        cells = [(r, c) for r in range(self.SIZE) for c in range(self.SIZE)]
        self.rng.shuffle(cells)
        removed = 0
        for r, c in cells:
            if removed >= holes:
                break
            backup = puzzle[r][c]
            puzzle[r][c] = 0
            if SudokuSolver.count_solutions(puzzle, limit=2) == 1:
                removed += 1
            else:
                puzzle[r][c] = backup
        return removed >= holes