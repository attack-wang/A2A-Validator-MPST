    def undo_move(self, move, undo):
        sr, sc = move.start
        er, ec = move.end
        piece = move.piece
        # Restore the moving piece (or the original pawn if promotion happened)
        if undo['promoted']:
            self.grid[sr][sc] = piece
            piece.has_moved = undo['piece_prev_has_moved']
        else:
            self.grid[sr][sc] = piece
            piece.has_moved = undo['piece_prev_has_moved']
        # Restore destination square
        self.grid[er][ec] = undo['captured']
        # Restore en passant captured pawn
        if undo['ep_captured'] is not None:
            cap_row, cap_col = sr, ec
            self.grid[cap_row][cap_col] = undo['ep_captured']
        # Restore rook for castling
        if undo['rook'] is not None:
            rook, rook_from, rook_to, rook_prev = undo['rook']
            self.grid[rook_to] = None
            self.grid[rook_from] = rook
            rook.has_moved = rook_prev
        # Restore state
        self.en_passant_target = undo['prev_ep']
        self.castling_rights = undo['prev_castling']
        self.halfmove_clock = undo['prev_halfmove']
        self.turn = undo['prev_turn']
        if self.move_history:
            self.move_history.pop()