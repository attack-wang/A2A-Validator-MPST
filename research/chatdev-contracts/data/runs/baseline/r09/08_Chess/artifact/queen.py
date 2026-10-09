class Bishop(Piece):
    LETTER = 'B'
    DIRECTIONS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    def pseudo_moves(self, board, file, rank):
        return self._slide(board, file, rank, self.DIRECTIONS)
    def _slide(self, board, file, rank, directions):
        moves = []
        for df, dr in directions:
            step = 1
            while True:
                target = (file + df * step, rank + dr * step)
                if not board.is_inside(*target):
                    break
                occupant = board.get_piece(*target)
                if occupant is None:
                    self._add(moves, board, (file, rank), target)
                else:
                    if occupant.color != self.color:
                        self._add(moves, board, (file, rank), target, captured=occupant)
                    break
                step += 1
        return moves
class Rook(Piece):
    LETTER = 'R'
    DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    # same _slide
class Queen(Piece):
    LETTER = 'Q'
    DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]