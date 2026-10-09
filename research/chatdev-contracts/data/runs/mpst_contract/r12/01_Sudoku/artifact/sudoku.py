"""Sudoku board logic: generation, validation and display for a 9x9 grid."""

import random


class SudokuBoard:
    def __init__(self, clues=38):
        self.grid = [[0] * 9 for _ in range(9)]
        self.fixed = [[False] * 9 for _ in range(9)]
        self._generate(clues)

    # --- generation -----------------------------------------------------
    def _fits(self, grid, r, c, v):
        for i in range(9):
            if i != c and grid[r][i] == v:
                return False
            if i != r and grid[i][c] == v:
                return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if (i, j) != (r, c) and grid[i][j] == v:
                    return False
        return True

    def _fill(self, grid, pos=0):
        if pos == 81:
            return True
        r, c = divmod(pos, 9)
        if grid[r][c]:
            return self._fill(grid, pos + 1)
        for v in random.sample(range(1, 10), 9):
            if self._fits(grid, r, c, v):
                grid[r][c] = v
                if self._fill(grid, pos + 1):
                    return True
                grid[r][c] = 0
        return False

    def _generate(self, clues):
        full = [[0] * 9 for _ in range(9)]
        self._fill(full)
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        for r, c in cells[:81 - clues]:
            full[r][c] = 0
        self.grid = full
        self.fixed = [[full[r][c] != 0 for c in range(9)] for r in range(9)]

    # --- gameplay -------------------------------------------------------
    def is_fixed(self, r, c):
        return self.fixed[r][c]

    def is_valid_move(self, r, c, v):
        return self._fits(self.grid, r, c, v)

    def set_cell(self, r, c, v):
        if not self.fixed[r][c]:
            self.grid[r][c] = v

    def clear_cell(self, r, c):
        if not self.fixed[r][c]:
            self.grid[r][c] = 0

    def find_mistakes(self):
        return [(r, c) for r in range(9) for c in range(9)
                if self.grid[r][c] and not self._fits(self.grid, r, c, self.grid[r][c])]

    def is_complete(self):
        return (all(self.grid[r][c] for r in range(9) for c in range(9))
                and not self.find_mistakes())

    # --- display --------------------------------------------------------
    def display(self):
        print("    1 2 3   4 5 6   7 8 9")
        for r in range(9):
            if r and r % 3 == 0:
                print("  " + "-" * 25)
            cells = []
            for c in range(9):
                if c and c % 3 == 0:
                    cells.append("|")
                cells.append(str(self.grid[r][c]) if self.grid[r][c] else ".")
            cells.append("|")
            print(f"{r + 1} " + " ".join(cells))
        print("  " + "-" * 25)