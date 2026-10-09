'''
SudokuBoard: game model for the Sudoku puzzle.
Stores the puzzle clues, the solution, and the player's entries, and
provides validation, conflict detection, hints, and completion checks.
'''
import random
class SudokuBoard:
    def __init__(self, puzzle, solution):
        self.puzzle = [row[:] for row in puzzle]
        self.solution = [row[:] for row in solution]
        self.given = [[self.puzzle[r][c] != 0 for c in range(9)] for r in range(9)]
        self.user_values = [[0 for _ in range(9)] for _ in range(9)]
    def is_given(self, row, col):
        """Return True if the cell at (row, col) is a pre-filled clue."""
        return self.given[row][col]
    def get_value(self, row, col):
        """Return the current displayed value: clue if given, else user entry."""
        if self.given[row][col]:
            return self.puzzle[row][col]
        return self.user_values[row][col]
    def set_value(self, row, col, value):
        """Set a user value at (row, col); ignored for given cells or invalid digits."""
        if self.given[row][col]:
            return False
        if value is None or value < 0 or value > 9:
            return False
        self.user_values[row][col] = value
        return True
    def clear_value(self, row, col):
        """Clear the user value at (row, col); given cells cannot be cleared."""
        if self.given[row][col]:
            return False
        self.user_values[row][col] = 0
        return True
    def clear_all_user_values(self):
        """Reset every user entry to empty, keeping the original clues."""
        for r in range(9):
            for c in range(9):
                if not self.given[r][c]:
                    self.user_values[r][c] = 0
    def count_empty(self):
        """Return the number of cells that currently hold no value."""
        return sum(1 for r in range(9) for c in range(9) if self.get_value(r, c) == 0)
    def get_conflicts(self, row, col):
        """Return a set of (r, c) cells conflicting with the value at (row, col)."""
        value = self.get_value(row, col)
        conflicts = set()
        if value == 0:
            return conflicts
        for c in range(9):
            if c != col and self.get_value(row, c) == value:
                conflicts.add((row, c))
        for r in range(9):
            if r != row and self.get_value(r, col) == value:
                conflicts.add((r, col))
        br, bc = (row // 3) * 3, (col // 3) * 3
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if (r, c) != (row, col) and self.get_value(r, c) == value:
                    conflicts.add((r, c))
        return conflicts
    def get_all_conflicts(self):
        """Return the set of all cells currently involved in any rule conflict."""
        conflicts = set()
        for r in range(9):
            for c in range(9):
                if self.get_value(r, c) != 0:
                    conflicts |= self.get_conflicts(r, c)
        return conflicts
    def is_full(self):
        """Return True when every cell holds a non-zero value."""
        return self.count_empty() == 0
    def is_filled_correctly(self):
        """Return True when the grid is full and every entry matches the solution."""
        if not self.is_full():
            return False
        for r in range(9):
            for c in range(9):
                if self.get_value(r, c) != self.solution[r][c]:
                    return False
        return True
    def get_hint(self):
        """Return (row, col, correct_value) for a random incorrect/empty cell, or None."""
        candidates = []
        for r in range(9):
            for c in range(9):
                if not self.given[r][c] and self.get_value(r, c) != self.solution[r][c]:
                    candidates.append((r, c))
        if not candidates:
            return None
        row, col = random.choice(candidates)
        return (row, col, self.solution[row][col])