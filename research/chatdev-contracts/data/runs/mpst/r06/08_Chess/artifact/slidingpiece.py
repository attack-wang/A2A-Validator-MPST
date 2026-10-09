class SlidingPiece(Piece):
    DIRECTIONS = ()
    def pseudo_legal_moves(self, board, row, col):
        moves = []
        for dr, dc in self.DIRECTIONS:
            r, c = row+dr, col+dc
            while board.in_bounds(r, c):
                t = board.get((r,c))
                if t is None:
                    moves.append(Move((row,col),(r,c),self))
                else:
                    if t.color != self.color:
                        moves.append(Move((row,col),(r,c),self,captured=t))
                    break
                r += dr; c += dc
        return moves
class Bishop(SlidingPiece): DIRECTIONS = diagonals
class Rook(SlidingPiece): DIRECTIONS = orthogonals
class Queen(SlidingPiece): DIRECTIONS = all 8