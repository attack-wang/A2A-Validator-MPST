class Slider(Piece):
    def __init__(self, color, symbol, directions):
        super().__init__(color, symbol)
        self.directions = directions
    def pseudo_moves(self, board, row, col):
        moves = []
        for dr, dc in self.directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board.grid[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves