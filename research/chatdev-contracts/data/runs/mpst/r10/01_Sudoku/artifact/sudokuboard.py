class SudokuBoard:
    def __init__(self, puzzle=None, solution=None):
        self.puzzle = [row[:] for row in puzzle] if puzzle else [[EMPTY]*9 for _ in range(9)]
        self.solution = [row[:] for row in solution] if solution else None
        self.entries = [[EMPTY]*9 for _ in range(9)]
        # initialize entries with puzzle clues
        for r in range(9):
            for c in range(9):
                if self.puzzle[r][c] != EMPTY:
                    self.entries[r][c] = self.puzzle[r][c]
    def is_fixed_cell(self, row, col):
        return self.puzzle[row][col] != EMPTY
    def get_value(self, row, col):
        return self.entries[row][col]
    def set_value(self, row, col, value):
        """Set player value; returns False if cell is fixed or value invalid."""
        if self.is_fixed_cell(row, col):
            return False
        if value == EMPTY or value in DIGITS:
            self.entries[row][col] = value
            return True
        return False
    def clear_value(self, row, col):
        if not self.is_fixed_cell(row, col):
            self.entries[row][col] = EMPTY
    def reset_player_entries(self):
        for r in range(9):
            for c in range(9):
                if not self.is_fixed_cell(r, c):
                    self.entries[r][c] = EMPTY
    def is_placement_valid(self, row, col, value):
        """Check whether `value` can be placed at (row, col) ignoring the current content of that cell."""
        if value == EMPTY:
            return True
        # row
        for c in range(9):
            if c != col and self.entries[row][c] == value:
                return False
        # column
        for r in range(9):
            if r != row and self.entries[r][col] == value:
                return False
        # box
        br, bc = (row // 3) * 3, (col // 3) * 3
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if (r, c) != (row, col) and self.entries[r][c] == value:
                    return False
        return True
    def find_conflicts(self):
        """Return set of (row, col) cells that violate Sudoku rules."""
        conflicts = set()
        # rows
        for r in range(9):
            seen = {}
            for c in range(9):
                v = self.entries[r][c]
                if v != EMPTY:
                    if v in seen:
                        conflicts.add((r, seen[v]))
                        conflicts.add((r, c))
                    else:
                        seen[v] = c
        # cols
        for c in range(9):
            seen = {}
            for r in range(9):
                v = self.entries[r][c]
                if v != EMPTY:
                    if v in seen:
                        conflicts.add((seen[v], c))
                        conflicts.add((r, c))
                    else:
                        seen[v] = r
        # boxes
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                seen = {}
                for r in range(br, br+3):
                    for c in range(bc, bc+3):
                        v = self.entries[r][c]
                        if v != EMPTY:
                            if v in seen:
                                conflicts.add(seen[(r,c)])  # hmm need to store coords