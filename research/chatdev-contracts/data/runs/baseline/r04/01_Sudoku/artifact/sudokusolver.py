'''
sudoku_engine.py
Core game logic for the classic Sudoku puzzle game.
This module is completely independent of any GUI framework and contains:
- SudokuSolver:    a backtracking solver used for generating puzzles,
                   verifying uniqueness, and revealing solutions.
- SudokuBoard:     the mutable game state (grid + fixed-cell mask) with
                   rule validation, conflict detection and completion checks.
- SudokuGenerator: random puzzle generation with guaranteed unique solutions
                   at several difficulty levels.
'''
import random
class SudokuSolver:
    """Backtracking solver/counter used by the generator and the GUI."""
    @staticmethod
    def _find_empty(grid):
        """Return (row, col) of the first empty cell, or None if full."""
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    return row, col
        return None
    @staticmethod
    def is_safe(grid, row, col, value):
        """Return True if `value` can be placed at (row, col) without
        violating the row, column or 3x3 subgrid rules."""
        if grid[row][col] == value:
            return True
        if value in grid[row]:
            return False
        for r in range(9):
            if grid[r][col] == value:
                return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if grid[r][c] == value:
                    return False
        return True