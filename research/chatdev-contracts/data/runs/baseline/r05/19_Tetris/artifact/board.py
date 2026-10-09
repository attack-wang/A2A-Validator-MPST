'''
board.py
Game board: grid state, collision detection, piece locking and
completed-line clearing.
'''
class Board:
    """Game board: grid state, collision detection, line clearing."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None] * width for _ in range(height)]
    def is_valid(self, matrix, x, y):
        """Check whether a piece matrix placed at (x, y) fits inside the board
        and does not collide with locked cells."""
        for row_i, row in enumerate(matrix):
            for col_i, cell in enumerate(row):
                if cell:
                    bx, by = x + col_i, y + row_i
                    if bx < 0 or bx >= self.width or by >= self.height:
                        return False
                    if by >= 0 and self.grid[by][bx] is not None:
                        return False
        return True
    def lock_piece(self, piece):
        """Write the piece's cells into the grid. Returns list of cleared line indices."""
        for (bx, by) in piece.cells():
            if by >= 0:
                self.grid[by][bx] = piece.color
        return self.clear_lines()
    def clear_lines(self):
        """Remove full rows, shift everything above down. Returns number of lines cleared."""
        full = [i for i, row in enumerate(self.grid) if all(row)]
        for i in full:
            del self.grid[i]
            self.grid.insert(0, [None] * self.width)
        return len(full)
    def is_top_out(self, piece):
        """Game over check: spawn position collides."""
        return not self.is_valid(piece.matrix, piece.x, piece.y)