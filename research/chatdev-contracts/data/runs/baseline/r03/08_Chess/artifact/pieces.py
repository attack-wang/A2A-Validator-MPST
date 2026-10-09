'''
Chess piece classes: base Piece and Pawn, Knight, Bishop, Rook, Queen, King.
Each piece generates pseudo-legal moves for a given board position.
'''
class Piece:
    def __init__(self, color):
        self.color = color  # 'white' or 'black'
        self.has_moved = False
    def display(self):
        raise NotImplementedError
    def pseudo_legal_moves(self, board, row, col):
        raise NotImplementedError
    def _slide_moves(self, board, row, col, directions):
        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while board.is_on_board(r, c):
                target = board.get_piece(r, c)
                if target is None:
                    moves.append((r, c))
                else:
                    if target.color != self.color:
                        moves.append((r, c))
                    break
                r += dr
                c += dc
        return moves
class Pawn(Piece):
    def display(self):
        return 'P' if self.color == 'white' else 'p'
    def pseudo_legal_moves(self, board, row, col):
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1
        # forward one
        r = row + direction
        if board.is_on_board(r, col) and board.get_piece(r, col) is None:
            moves.append((r, col))
            # forward two from start
            r2 = row + 2 * direction
            if row == start_row and board.get_piece(r2, col) is None:
                moves.append((r2, col))
        # captures
        for dc in (-1, 1):
            c = col + dc
            r = row + direction
            if not board.is_on_board(r, c):
                continue
            target = board.get_piece(r, c)
            if target is not None and target.color != self.color:
                moves.append((r, c))
        # en passant
        ep = board.en_passant_target
        if ep is not None:
            er, ec = ep
            if er == row + direction and abs(ec - col) == 1:
                if board.get_piece(er, ec) is None:
                    adjacent = board.get_piece(row, ec)
                    if isinstance(adjacent, Pawn) and adjacent.color != self.color:
                        moves.append((er, ec))
        return moves
class Knight(Piece):
    def display(self):
        return 'N' if self.color == 'white' else 'n'
    def pseudo_legal_moves(self, board, row, col):
        moves = []
        offsets = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        for dr, dc in offsets:
            r, c = row + dr, col + dc
            if board.is_on_board(r, c):
                target = board.get_piece(r, c)
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves
class Bishop(Piece):
    def display(self):
        return 'B' if self.color == 'white' else 'b'
    def pseudo_legal_moves(self, board, row, col):
        return self._slide_moves(board, row, col,
                                 [(-1,-1),(-1,1),(1,-1),(1,1)])
class Rook(Piece):
    def display(self):
        return 'R' if self.color == 'white' else 'r'
    def pseudo_legal_moves(self, board, row, col):
        return self._slide_moves(board, row, col,
                                 [(-1,0),(1,0),(0,-1),(0,1)])
class Queen(Piece):
    def display(self):
        return 'Q' if self.color == 'white' else 'q'
    def pseudo_legal_moves(self, board, row, col):
        return self._slide_moves(board, row, col,
                                 [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)])
class King(Piece):
    def display(self):
        return 'K' if self.color == 'white' else 'k'
    def pseudo_legal_moves(self, board, row, col):
        moves = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if board.is_on_board(r, c):
                    target = board.get_piece(r, c)
                    if target is None or target.color != self.color:
                        moves.append((r, c))
        # castling handled at board level via castling_destinations
        moves.extend(board.castling_destinations(self, row, col))
        return moves