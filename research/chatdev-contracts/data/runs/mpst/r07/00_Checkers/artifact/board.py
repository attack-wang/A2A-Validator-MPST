    def get(self, r, c):
        if not self.in_bounds(r, c):
            return None
        return self.grid[r][c]
    def set(self, r, c, piece):
        self.grid[r][c] = piece
    def remove(self, r, c):
        self.grid[r][c] = None
    def move_piece(self, start, end):
        """Low-level relocation of a piece from `start` to `end` (no rule checks)."""
        piece = self.get(*start)
        self.remove(*start)
        self.set(end[0], end[1], piece)
        return piece
    def display(self):
        """Render the board with file letters a-h and rank numbers 1-8."""
        lines = []
        header = "    " + "   ".join("abcdefgh")  # hmm, need to align with cell width
        ...