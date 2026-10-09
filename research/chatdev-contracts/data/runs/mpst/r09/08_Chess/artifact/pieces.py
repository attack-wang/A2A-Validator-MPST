class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'K')
    def pseudo_moves(self, board, row, col):
        moves = []
        for dr, dc in KING_DIRS:
            r, c = row+dr, col+dc
            if 0 <= r < 8 and 0 <= c < 8:
                t = board.grid[r][c]
                if t is None or t.color != self.color:
                    moves.append((r, c))
        return moves