'''
Pawn piece: forward moves, double push, captures, en passant.
'''
from piece import Piece
class Pawn(Piece):
    letter = 'P'
    value = 1
    def pseudo_moves(self, board, file, rank):
        moves = []
        direction = 1 if self.color == 'w' else -1
        start_rank = 1 if self.color == 'w' else 6
        one = rank + direction
        if 0 <= one <= 7 and board.grid[one][file] is None:
            moves.append((file, one))
            two = rank + 2 * direction
            if rank == start_rank and board.grid[two][file] is None:
                moves.append((file, two))
        for df in (-1, 1):
            f = file + df
            r = rank + direction
            if 0 <= f <= 7 and 0 <= r <= 7:
                target = board.grid[r][f]
                if target is not None and target.color != self.color:
                    moves.append((f, r))
                elif board.en_passant_target == (f, r):
                    moves.append((f, r))
        return moves