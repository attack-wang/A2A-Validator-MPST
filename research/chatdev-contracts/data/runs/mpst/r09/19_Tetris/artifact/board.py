'''Game board: grid management, collision detection, line clearing.'''
from constants import BOARD_WIDTH, BOARD_HEIGHT
class Board:
    """Represents the Tetris playfield and manages locked cells."""
    def __init__(self):
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.reset()
    def reset(self):
        """Clear the board to its initial empty state."""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    def is_valid_position(self, piece, dx=0, dy=0):
        """Check whether the piece placed at (x+dx, y+dy) fits inside the board
        and does not collide with locked cells."""
        for cell_x, cell_y in piece.cells():
            new_x = cell_x + dx
            new_y = cell_y + dy
            if new_x < 0 or new_x >= self.width or new_y >= self.height:
                return False
            if new_y >= 0 and self.grid[new_y][new_x] is not None:
                return False
        return True
    def lock_piece(self, piece):
        """Write the piece's cells into the grid. Returns True if any part of
        the piece is above the top of the board (lock out)."""
        lock_out = False
        for cell_x, cell_y in piece.cells():
            if cell_y < 0:
                lock_out = True
            else:
                self.grid[cell_y][cell_x] = piece.color
        return lock_out
    def clear_lines(self):
        """Remove all completed rows, shift rows above down.
        Returns the number of cleared lines."""
        cleared = 0
        new_grid = []
        for row in self.grid:
            if all(cell is not None for cell in row):
                cleared += 1
            else:
                new_grid.append(row)
        for _ in range(cleared):
            new_grid.insert(0, [None for _ in range(self.width)])
        self.grid = new_grid
        return cleared
    def is_top_reached(self, piece):
        """Game over check: a newly spawned piece overlaps locked cells."""
        return not self.is_valid_position(piece)