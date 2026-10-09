'''
Board module for the Tetris game.
Manages the grid, collision detection, piece locking, and line clearing.
'''
from constants import BOARD_WIDTH, BOARD_HEIGHT
class Board:
    """Represents the Tetris playfield as a grid of locked cells."""
    def __init__(self):
        """Create an empty board (None means no locked block in that cell)."""
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    def is_valid_position(self, cells):
        """Return True if all (x, y) cells are inside the board and unoccupied."""
        for (x, y) in cells:
            # Outside horizontal walls or below the floor -> invalid
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return False
            # Occupied by a locked block -> invalid
            if self.grid[y][x] is not None:
                return False
        return True
    def is_game_over(self, cells):
        """Return True if a newly spawned piece overlaps locked blocks."""
        for (x, y) in cells:
            if 0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] is not None:
                return True
        return False
    def lock_piece(self, cells, color_key):
        """Write the piece's color key into the grid at the given cells."""
        for (x, y) in cells:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y][x] = color_key
    def clear_lines(self):
        """Remove all full rows, shift rows down, and return the number cleared."""
        cleared = 0
        remaining = []
        for row in self.grid:
            if all(cell is not None for cell in row):
                cleared += 1
            else:
                remaining.append(row)
        # Add empty rows at the top to keep the board height constant
        while len(remaining) < self.height:
            remaining.insert(0, [None for _ in range(self.width)])
        self.grid = remaining
        return cleared