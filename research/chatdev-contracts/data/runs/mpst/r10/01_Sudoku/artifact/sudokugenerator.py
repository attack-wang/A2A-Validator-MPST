class SudokuGenerator:
    """Generates random, uniquely solvable Sudoku puzzles."""
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
    def generate(self, difficulty="Medium"):
        """Generate a puzzle for the given difficulty and return a SudokuBoard."""
        num_to_remove = DIFFICULTY_LEVELS.get(difficulty, DIFFICULTY_LEVELS["Medium"])
        solution = self._generate_full_solution()
        puzzle = [row[:] for row in solution]
        self._remove_cells(puzzle, num_to_remove)
        return SudokuBoard(puzzle=puzzle, solution=solution)
    def _generate_full_solution(self):
        board = [[EMPTY] * 9 for _ in range(9)]
        self._fill_board(board)
        return board
    def _fill_board(self, board):
        return self._backtrack_fill(board, 0)
    def _backtrack_fill(self, board, index):
        if index == 81:
            return True
        row, col = divmod(index, 9)
        values = list(range(1, 10))
        self.rng.shuffle(values)
        for value in values:
            if self._can_place(board, row, col, value):
                board[row][col] = value
                if self._backtrack_fill(board, index + 1):
                    return True
                board[row][col] = EMPTY
        return False
    @staticmethod
    def _can_place(board, row, col, value):
        for c in range(9):
            if board[row][c] == value:
                return False
        for r in range(9):
            if board[r][col] == value:
                return False
        br, bc = (row // 3) * 3, (col // 3) * 3
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if board[r][c] == value:
                    return False
        return True
    def _remove_cells(self, puzzle, num_to_remove):
        cells = [(r, c) for r in range(9) for c in range(9)]
        self.rng.shuffle(cells)
        removed = 0
        for row, col in cells:
            if removed >= num_to_remove:
                break
            backup = puzzle[row][col]
            puzzle[row][col] = EMPTY
            if self._count_solutions(puzzle, limit=2) != 1:
                puzzle[row][col] = backup
            else:
                removed += 1
        return removed
    def _count_solutions(self, board, limit=2):
        grid = [row[:] for row in board]
        count = 0
        def solve():
            nonlocal count
            best = None
            best_options = None
            # find the empty cell with the fewest candidates (MRV heuristic)
            for r in range(9):
                for c in range(9):
                    if grid[r][c] == EMPTY:
                        options = [v for v in range(1, 10) if self._can_place(grid, r, c, v)]
                        if not options:
                            return  # dead end
                        if best_options is None or len(options) < len(best_options):
                            best, best_options = (r, c), options
                            if len(options) == 1:
                                break  # can't do better
                if best_options is not None and len(best_options) == 1:
                    break
            if best is None:
                count += 1
                return
            r, c = best
            for v in best_options:
                grid[r][c] = v
                solve()
                grid[r][c] = EMPTY
                if count >= limit:
                    return
        solve()
        return count