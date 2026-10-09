class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'N')
    def pseudo_legal_moves(self, board, row, col):
        offsets = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        moves = []
        for dr, dc in offsets:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece(r, c)
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves