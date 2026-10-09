class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'P')
    def pseudo_legal_moves(self, board, row, col):
        moves = []
        direction = -1 if self.color == 'w' else 1
        start_row = 6 if self.color == 'w' else 1
        r = row + direction
        if 0 <= r < 8 and board.get_piece(r, col) is None:
            moves.append((r, col))
            r2 = row + 2 * direction
            if row == start_row and board.get_piece(r2, col) is None:
                moves.append((r2, col))
        for dc in (-1, 1):
            c = col + dc
            r = row + direction
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece(r, c)
                if target is not None and target.color != self.color:
                    moves.append((r, c))
                elif target is None and board.en_passant_target == (r, c):
                    moves.append((r, c))
        return moves