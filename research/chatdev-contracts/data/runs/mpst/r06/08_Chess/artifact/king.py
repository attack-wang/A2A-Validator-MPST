KING_OFFSETS = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
class King(Piece):
    def pseudo_legal_moves(self, board, row, col):
        moves = []
        for dr, dc in KING_OFFSETS:
            ...
        # castling
        opp = 'b' if self.color == 'w' else 'w'
        rank = 7 if self.color == 'w' else 0
        if (row, col) != (rank, 4): return moves  # king must be on e-file home square
        king_side = 'K' if self.color=='w' else 'k'
        queen_side = 'Q' if self.color=='w' else 'q'
        # king side: rook on h-file, squares f,g empty; e,f,g not attacked
        if board.castling_rights.get(king_side):
            rook = board.get((rank, 7))
            if rook is not None and rook.type == 'rook' and rook.color == self.color:
                if board.get((rank,5)) is None and board.get((rank,6)) is None:
                    if not board.is_attacked((rank,4), opp) and not board.is_attacked((rank,5), opp) and not board.is_attacked((rank,6), opp):
                        moves.append(Move((rank,4),(rank,6),self,is_castle_king=True))
        if board.castling_rights.get(queen_side):
            rook = board.get((rank, 0))
            if rook is not None and rook.type=='rook' and rook.color==self.color:
                if board.get((rank,1)) is None and board.get((rank,2)) is None and board.get((rank,3)) is None:
                    if not board.is_attacked((rank,4),opp) and not board.is_attacked((rank,3),opp) and not board.is_attacked((rank,2),opp):
                        moves.append(Move((rank,4),(rank,2),self,is_castle_queen=True))
        return moves