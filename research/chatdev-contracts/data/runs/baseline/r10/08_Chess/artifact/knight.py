class Knight(Piece):
    letter = 'N'
    value = 3
    OFFSETS = [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
    def pseudo_moves(self, board, file, rank):
        moves = []
        for df, dr in self.OFFSETS:
            f, r = file + df, rank + dr
            if 0 <= f <= 7 and 0 <= r <= 7:
                target = board.grid[r][f]
                if target is None or target.color != self.color:
                    moves.append((f, r))
        return moves