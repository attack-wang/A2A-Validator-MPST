'''
King piece: one-step moves; castling handled by Board.
'''
from piece import Piece
class King(Piece):
    letter = 'K'
    value = 0
    def pseudo_moves(self, board, file, rank):
        moves = []
        for df in (-1, 0, 1):
            for dr in (-1, 0, 1):
                if df == 0 and dr == 0:
                    continue
                f, r = file + df, rank + dr
                if 0 <= f <= 7 and 0 <= r <= 7:
                    target = board.grid[r][f]
                    if target is None or target.color != self.color:
                        moves.append((f, r))
        return moves