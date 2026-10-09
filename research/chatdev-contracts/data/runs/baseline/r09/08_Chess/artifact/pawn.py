class Pawn(Piece):
    LETTER = 'P'
    def pseudo_moves(self, board, file, rank):
        moves = []
        direction = 1 if self.color == 'w' else -1
        start_rank = 1 if self.color == 'w' else 6
        # single push
        one = (file, rank + direction)
        if board.is_inside(*one) and board.get_piece(*one) is None:
            self._add(moves, board, (file, rank), one)
            # double push
            two = (file, rank + 2 * direction)
            if rank == start_rank and board.get_piece(*two) is None:
                self._add(moves, board, (file, rank), two, flag='double')
        # captures
        for df in (-1, 1):
            target = (file + df, rank + direction)
            if not board.is_inside(*target):
                continue
            occupant = board.get_piece(*target)
            if occupant is not None and occupant.color != self.color:
                self._add(moves, board, (file, rank), target, captured=occupant)
            elif board.en_passant_target == target:
                ep_pawn = board.get_piece(target[0], rank)  # pawn beside us
                self._add(moves, board, (file, rank), target, captured=ep_pawn, flag='ep')
        return moves