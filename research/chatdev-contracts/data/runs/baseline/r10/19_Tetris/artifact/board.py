'''
board.py
Defines the Board class managing the 10x20 grid, collision detection, line clearing, and rendering.
'''
import pygame
from constants import (CELL_SIZE, COLS, ROWS, GRID_LINE, DARK_GRAY, BLACK)
class Board:
    """The Tetris playfield: a grid that stores locked cells and handles collisions."""
    def __init__(self):
        # Grid holds None for empty cells or an (R, G, B) color tuple
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    def reset(self):
        """Clear the board for a new game."""
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
    def is_inside(self, col, row):
        """Check whether a cell coordinate lies within the board bounds."""
        return 0 <= col < COLS and 0 <= row < ROWS
    def is_valid_position(self, tetromino, dx=0, dy=0):
        """Check if the tetromino (optionally moved by dx, dy) fits without collision.
        Cells above the top edge (row < 0) are allowed as long as the columns
        are within bounds; the grid is only consulted for rows inside the board.
        """
        for col, row in tetromino.get_cells():
            c, r = col + dx, row + dy
            if c < 0 or c >= COLS or r >= ROWS:
                return False
            if r >= 0 and self.grid[r][c] is not None:
                return False
        return True
    def lock_tetromino(self, tetromino):
        """Write the tetromino's cells into the grid (called when it lands)."""
        for col, row in tetromino.get_cells():
            if row >= 0:
                self.grid[row][col] = tetromino.color
    def clear_lines(self):
        """Remove fully occupied rows, shift everything above down; return number cleared."""
        cleared = 0
        new_grid = []
        for row in self.grid:
            if all(cell is not None for cell in row):
                cleared += 1
            else:
                new_grid.append(row)
        # Add empty rows at the top for each cleared line
        for _ in range(cleared):
            new_grid.insert(0, [None for _ in range(COLS)])
        self.grid = new_grid
        return cleared
    def is_game_over(self, tetromino):
        """Game over if a freshly spawned piece collides immediately at spawn."""
        return not self.is_valid_position(tetromino)
    def draw(self, surface, offset_x=0):
        """Render the board background, grid lines, and locked cells."""
        # Board background
        pygame.draw.rect(surface, BLACK, (offset_x, 0, COLS * CELL_SIZE, ROWS * CELL_SIZE))
        # Grid lines
        for c in range(COLS + 1):
            pygame.draw.line(surface, GRID_LINE,
                             (offset_x + c * CELL_SIZE, 0),
                             (offset_x + c * CELL_SIZE, ROWS * CELL_SIZE))
        for r in range(ROWS + 1):
            pygame.draw.line(surface, GRID_LINE,
                             (offset_x, r * CELL_SIZE),
                             (offset_x + COLS * CELL_SIZE, r * CELL_SIZE))
        # Locked cells
        for r in range(ROWS):
            for c in range(COLS):
                color = self.grid[r][c]
                if color:
                    rect = pygame.Rect(offset_x + c * CELL_SIZE, r * CELL_SIZE,
                                       CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(surface, color, rect)
                    pygame.draw.rect(surface, DARK_GRAY, rect, 1)