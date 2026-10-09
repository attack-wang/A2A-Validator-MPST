class Pawn(Piece):
    @property
    def letter(self):
        return ''
    @property
    def value(self):
        return 1
    def unicode_symbol(self):
        return '♙' if self.color == 'w' else '♟'
    def ascii_symbol(self):
        return 'P' if self.color == 'w' else 'p'
    def pseudo_legal_moves(self, board, row, col, game):
        moves = []
        direction = -1 if self.color == 'w' else 1
        start_row = 6 if self.color == 'w' else 1
        promo_row = 0 if self.color == 'w' else 7
        # Forward one
        r1 = row + direction
        if 0 <= r1 < 8 and board.grid[r1][col] is None:
            moves.append(Move((row, col), (r1, col), promotion_needed=(r1 == promo_row)))
            # Forward two
            r2 = row + 2 * direction
            if row == start_row and board.grid[r2][col] is None:
                moves.append(Move((row, col), (r2, col)))
        # Captures
        for dc in (-1, 1):
            c1 = col + dc
            if 0 <= c1 < 8 and 0 <= r1 < 8:
                target = board.grid[r1][c1]
                if target is not None and target.color != self.color:
                    moves.append(Move((row, col), (r1, c1), promotion_needed=(r1 == promo_row)))
                # En passant
                elif game.en_passant_target == (r1, c1):
                    moves.append(Move((row, col), (r1, c1), is_en_passant=True))
        return moves