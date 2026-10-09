'''
board.py
Defines the Board class, the 10x20 playfield.
The board owns the grid of locked cells and provides collision testing,
piece locking, line clearing, and game-over detection.
'''
from settings import COLS, ROWS, WALL_KICK_OFFSETS
class Board:
    """The Tetris playfield: a grid of locked cells plus collision logic."""
    def __init__(self):
        """Create an empty board."""
        self.cols = COLS
        self.rows = ROWS
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
    # ------------------------------------------------------------------
    # Collision / validity
    # ------------------------------------------------------------------
    def is_valid_position(self, tetromino, offset_x=0, offset_y=0, matrix=None):
        """
        Return True if the tetromino (optionally shifted by the given
        offsets and/or using an alternative rotation matrix) fits entirely
        inside the board without overlapping locked cells.
        """
        if matrix is None:
            matrix = tetromino.matrix
        for cell_x, cell_y in tetromino.get_cells(offset_x, offset_y, matrix):
            if cell_x < 0 or cell_x >= self.cols:
                return False
            if cell_y >= self.rows:
                return False
            if cell_y >= 0 and self.grid[cell_y][cell_x] is not None:
                return False
        return True
    # ------------------------------------------------------------------
    # Locking and clearing
    # ------------------------------------------------------------------
    def lock_piece(self, tetromino):
        """
        Merge the tetromino's cells into the grid permanently.
        Returns True if any part of the piece ended up above the top of
        the board (a lock-out condition the game can treat as game over).
        """
        for cell_x, cell_y in tetromino.get_cells():
            if cell_y < 0:
                return True
            self.grid[cell_y][cell_x] = tetromino.color
        return False
    def clear_lines(self):
        """
        Remove every fully occupied row.
        Returns the number of rows cleared (0-4). Remaining rows are
        shifted down and empty rows are added at the top.
        """
        full_rows = [row for row in range(self.rows)
                     if all(cell is not None for cell in self.grid[row])]
        for row in full_rows:
            del self.grid[row]
            self.grid.insert(0, [None for _ in range(self.cols)])
        return len(full_rows)
    def is_game_over(self, tetromino):
        """
        Return True if the freshly spawned tetromino already collides,
        meaning no more pieces can be placed and the game must end.
        """
        return not self.is_valid_position(tetromino)
    def reset(self):
        """Wipe the board back to an empty state (used on restart)."""
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]