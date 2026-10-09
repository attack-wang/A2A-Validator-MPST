class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'K')
    def pseudo_legal_moves(self, board, row, col):
        moves = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = board.get_piece(r, c)
                    if target is None or target.color != self.color:
                        moves.append((r, c))
        return moves