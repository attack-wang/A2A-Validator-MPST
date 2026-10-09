    def lock_current_piece(self):
        """Lock the piece, clear lines, update score/level, spawn the next piece."""
        cells = self.current_piece.get_cells()
        self.board.lock_piece(self.current_piece)
        # Lock out: any cell locked above the visible board ends the game
        if any(y < 0 for (x, y) in cells):
            self.game_over = True
            self.current_piece = None
            return