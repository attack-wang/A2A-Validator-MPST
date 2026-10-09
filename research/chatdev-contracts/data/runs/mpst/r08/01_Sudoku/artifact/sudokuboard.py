class SudokuBoard:
    def __init__(self, puzzle, solution):
        self.puzzle = [row[:] for row in puzzle]
        self.solution = [row[:] for row in solution]
        self.grid = [row[:] for row in puzzle]
    def is_fixed(self, row, col):
        return self.puzzle[row][col] != 0
    def get_value(self, row, col):
        return self.grid[row][col]
    def set_value(self, row, col, value):
        if self.is_fixed(row, col):
            return False
        if value is None:
            self.grid[row][col] = 0
            return True
        value = int(value)
        if not 1 <= value <= 9:
            return False
        self.grid[row][col] = value
        return True
    def clear_value(self, row, col):
        if not self.is_fixed(row, col):
            self.grid[row][col] = 0
    def has_conflict(self, row, col):
        value = self.grid[row][col]
        if value == 0:
            return False
        for c in range(9):
            if c != col and self.grid[row][c] == value:
                return True
        for r in range(9):
            if r != row and self.grid[r][col] == value:
                return True
        br, bc = 3 * (row // 3), 3 * (col // 3)
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if (r, c) != (row, col) and self.grid[r][c] == value:
                    return True
        return False
    def find_mistakes(self):
        return [(r, c) for r in range(9) for c in range(9)
                if self.grid[r][c] != 0 and self.has_conflict(r, c)]
    def find_empty_cells(self):
        return [(r, c) for r in range(9) for c in range(9) if self.grid[r][c] == 0]
    def is_complete(self):
        if self.find_empty_cells():
            return False
        return not self.find_mistakes()
    def is_cell_correct(self, row, col):
        return self.grid[row][col] == self.solution[row][col]
    def reveal_solution(self):
        self.grid = [row[:] for row in self.solution]