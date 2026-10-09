class SudokuBoard:
    SIZE = 9
    def __init__(self, puzzle=None):
        self.grid = [[0]*9 for _ in range(9)]
        self.fixed = [[False]*9 for _ in range(9)]
        if puzzle:
            self.load_puzzle(puzzle)
    def load_puzzle(self, puzzle):
        for r in range(9):
            for c in range(9):
                self.grid[r][c] = puzzle[r][c]
                self.fixed[r][c] = puzzle[r][c] != 0
    def get_cell(self, row, col):
        return self.grid[row][col]
    def set_cell(self, row, col, value):
        if self.fixed[row][col]:
            return False
        self.grid[row][col] = value
        return True
    def clear_cell(self, row, col):
        if not self.fixed[row][col]:
            self.grid[row][col] = 0
    def is_fixed(self, row, col):
        return self.fixed[row][col]
    def is_valid_placement(self, row, col, value):
        # Check whether placing value at (row, col) violates Sudoku rules
        # (ignoring the cell's own current value)
        for c in range(9):
            if c != col and self.grid[row][c] == value:
                return False
        for r in range(9):
            if r != row and self.grid[r][col] == value:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if (r, c) != (row, col) and self.grid[r][c] == value:
                    return False
        return True
    def find_conflicts(self):
        # Return a set of (row, col) cells that conflict with another cell
        conflicts = set()
        # rows
        for r in range(9):
            seen = {}
            for c in range(9):
                v = self.grid[r][c]
                if v != 0:
                    if v in seen:
                        conflicts.add((r, c))
                        conflicts.add((r, seen[v]))
                    else:
                        seen[v] = c
        # columns
        for c in range(9):
            seen = {}
            for r in range(9):
                v = self.grid[r][c]
                if v != 0:
                    if v in seen:
                        conflicts.add((r, c))
                        conflicts.add((seen[v], c))
                    else:
                        seen[v] = r
        # boxes
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                seen = {}
                for r in range(box_row, box_row+3):
                    for c in range(box_col, box_col+3):
                        v = self.grid[r][c]
                        if v != 0:
                            if v in seen:
                                conflicts.add((r, c))
                                conflicts.add(seen[v])
                            else:
                                seen[v] = (r, c)
        return conflicts
    def is_complete(self):
        # all cells filled and no conflicts
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    return False
        return len(self.find_conflicts()) == 0
    def is_correct(self, solution):
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] != solution[r][c]:
                    return False
        return True