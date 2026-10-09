KNIGHT_OFFSETS = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
class Knight(Piece):
    def pseudo_legal_moves(self, board, row, col):
        moves = []
        for dr, dc in KNIGHT_OFFSETS:
            r, c = row+dr, col+dc
            if board.in_bounds(r, c):
                t = board.get((r,c))
                if t is None or t.color != self.color:
                    moves.append(Move((row,col),(r,c),self,captured=t))
        return moves