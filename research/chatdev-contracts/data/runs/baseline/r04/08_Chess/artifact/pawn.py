class Pawn(Piece):
    value = 1
    letter = ''
    @property
    def unicode(self):
        return '♙' if self.color == WHITE else '♟'
    def pseudo_moves(self, board, row, col, game):
        moves = []
        direction = -1 if self.color == WHITE else 1  # white moves up (towards row 0)
        start_row = 6 if self.color == WHITE else 1
        # single push
        r = row + direction
        if 0 <= r < 8 and board.get_piece(r, col) is None:
            moves.append((r, col))
            # double push
            if row == start_row:
                r2 = row + 2 * direction
                if board.get_piece(r2, col) is None:
                    moves.append((r2, col))
        # captures
        for dc in (-1, 1):
            c = col + dc
            r = row + direction
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece(r, c)
                if target is not None and target.color != self.color:
                    moves.append((r, c))
                elif target is None and game.en_passant_target == (r, c):
                    moves.append((r, c))
        return moves