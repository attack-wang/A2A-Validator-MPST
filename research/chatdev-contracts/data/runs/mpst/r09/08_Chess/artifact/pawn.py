class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'P')
    def pseudo_moves(self, board, row, col):
        moves = []
        direction = -1 if self.color == 'w' else 1
        start_row = 6 if self.color == 'w' else 1
        # single push
        r = row + direction
        if 0 <= r < 8 and board.grid[r][col] is None:
            moves.append((r, col))
            # double push
            r2 = row + 2*direction
            if row == start_row and board.grid[r2][col] is None:
                moves.append((r2, col))
        # captures
        for dc in (-1, 1):
            r, c = row + direction, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                t = board.grid[r][c]
                if t is not None and t.color != self.color:
                    moves.append((r, c))
        return moves