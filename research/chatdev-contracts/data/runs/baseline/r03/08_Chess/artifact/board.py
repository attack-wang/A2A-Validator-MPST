'''
Board class: 8x8 grid, initial setup, move generation, legality checking,
make/undo move with full support for castling, en passant and promotion.
'''
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
from move import Move
class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.en_passant_target = None
        self.last_move = None
        self.setup()
    def setup(self):
        back = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for c in range(8):
            self.grid[0][c] = back[c]('black')
            self.grid[1][c] = Pawn('black')
            self.grid[6][c] = Pawn('white')
            self.grid[7][c] = back[c]('white')
    def display(self):
        # print with file/rank labels; white at bottom (rank 1)
        print()
        print('    a   b   c   d   e   f   g   h')
        print('  +---+---+---+---+---+---+---+---+')
        for r in range(8):
            rank = 8 - r
            row_str = f'{rank} |'
            for c in range(8):
                p = self.grid[r][c]
                row_str += f' {p.display() if p else "."} |'
            print(row_str)
            print('  +---+---+---+---+---+---+---+---+')
        print()
    def is_on_board(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8
    def get_piece(self, r, c):
        return self.grid[r][c]
    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if isinstance(p, King) and p.color == color:
                    return (r, c)
        return None
    def is_square_attacked(self, r, c, by_color):
        # pawn attacks
        direction = 1 if by_color == 'white' else -1
        # a white pawn attacks upward (towards lower row index), so a square (r,c)
        # is attacked by a white pawn at (r+1, c±1)
        for dc in (-1, 1):
            pr, pc = r + direction, c + dc
            if self.is_on_board(pr, pc):
                p = self.grid[pr][pc]
                if isinstance(p, Pawn) and p.color == by_color:
                    return True
        # knight attacks
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            kr, kc = r + dr, c + dc
            if self.is_on_board(kr, kc):
                p = self.grid[kr][kc]
                if isinstance(p, Knight) and p.color == by_color:
                    return True
        # king attacks (adjacent)
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                kr, kc = r + dr, c + dc
                if self.is_on_board(kr, kc):
                    p = self.grid[kr][kc]
                    if isinstance(p, King) and p.color == by_color:
                        return True
        # sliding attacks: rook/queen straight, bishop/queen diagonal
        straight = [(-1,0),(1,0),(0,-1),(0,1)]
        diagonal = [(-1,-1),(-1,1),(1,-1),(1,1)]
        for dr, dc in straight:
            rr, cc = r + dr, c + dc
            while self.is_on_board(rr, cc):
                p = self.grid[rr][cc]
                if p is not None:
                    if p.color == by_color and isinstance(p, (Rook, Queen)):
                        return True
                    break
                rr += dr
                cc += dc
        for dr, dc in diagonal:
            rr, cc = r + dr, c + dc
            while self.is_on_board(rr, cc):
                p = self.grid[rr][cc]
                if p is not None:
                    if p.color == by_color and isinstance(p, (Bishop, Queen)):
                        return True
                    break
                rr += dr
                cc += dc
        return False
    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if king_pos is None:
            return False
        enemy = 'black' if color == 'white' else 'white'
        return self.is_square_attacked(king_pos[0], king_pos[1], enemy)
    def castling_destinations(self, king, row, col):
        """Return castling destination squares for king at (row, col), if legal (pseudo-legal level)."""
        dests = []
        if not isinstance(king, King) or king.has_moved:
            return dests
        if self.is_in_check(king.color):  # can't castle out of check
            return dests
        enemy = 'black' if king.color == 'white' else 'white'
        row_expected = 7 if king.color == 'white' else 0
        if row != row_expected or col != 4:
            return dests
        # Kingside: rook at h-file
        rook = self.get_piece(row, 7)
        if (isinstance(rook, Rook) and rook.color == king.color and not rook.has_moved
                and self.get_piece(row, 5) is None and self.get_piece(row, 6) is None
                and not self.is_square_attacked(row, 5, enemy)
                and not self.is_square_attacked(row, 6, enemy)):
            dests.append((row, 6))
        # Queenside: rook at a-file
        rook = self.get_piece(row, 0)
        if (isinstance(rook, Rook) and rook.color == king.color and not rook.has_moved
                and self.get_piece(row, 1) is None and self.get_piece(row, 2) is None and self.get_piece(row, 3) is None
                and not self.is_square_attacked(row, 3, enemy)
                and not self.is_square_attacked(row, 2, enemy)):
            dests.append((row, 2))
        return dests
    def all_pseudo_legal_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if piece is not None and piece.color == color:
                    for (er, ec) in piece.pseudo_legal_moves(self, r, c):
                        move = self.build_move(r, c, er, ec)
                        if move.promotion_options:
                            for promo_cls in move.promotion_options:
                                promo_move = Move(move.start, move.end, move.piece,
                                                  captured=move.captured,
                                                  is_en_passant=move.is_en_passant,
                                                  promotion=promo_cls)
                                moves.append(promo_move)
                        else:
                            moves.append(move)
        return moves
    def build_move(self, sr, sc, er, ec):
        piece = self.grid[sr][sc]
        target = self.grid[er][ec]
        is_ep = False
        captured = target
        if isinstance(piece, Pawn) and target is None and sc != ec:
            # diagonal pawn move to an empty square can only be en passant
            is_ep = True
            captured = self.grid[sr][ec]
        move = Move((sr, sc), (er, ec), piece, captured=captured, is_en_passant=is_ep)
        if isinstance(piece, Pawn) and (er == 0 or er == 7):
            move.promotion_options = [Queen, Rook, Bishop, Knight]
        return move
    def legal_moves(self, color):
        legal = []
        for move in self.all_pseudo_legal_moves(color):
            self.make_move(move)
            if not self.is_in_check(color):
                legal.append(move)
            self.undo_move(move)
        return legal
    def make_move(self, move):
        sr, sc = move.start
        er, ec = move.end
        piece = move.piece
        move.prev_has_moved = piece.has_moved
        move.prev_en_passant_target = self.en_passant_target
        if move.is_en_passant:
            self.grid[sr][ec] = None
        self.grid[sr][sc] = None
        if move.promotion is not None:
            new_piece = move.promotion(piece.color)
            new_piece.has_moved = True
            self.grid[er][ec] = new_piece
        else:
            piece.has_moved = True
            self.grid[er][ec] = piece
        if move.is_castling:
            rr_s, rc_s = move.rook_start
            rr_e, rc_e = move.rook_end
            rook = self.grid[rr_s][rc_s]
            move.prev_rook_has_moved = rook.has_moved
            self.grid[rr_s][rc_s] = None
            rook.has_moved = True
            self.grid[rr_e][rc_e] = rook
        self.en_passant_target = ((sr + er) // 2, sc) if (isinstance(piece, Pawn) and abs(er - sr) == 2) else None
        self.last_move = move
    def undo_move(self, move):
        sr, sc = move.start
        er, ec = move.end
        piece = move.piece
        self.grid[sr][sc] = piece
        piece.has_moved = move.prev_has_moved
        self.grid[er][ec] = None
        if move.is_en_passant:
            self.grid[sr][ec] = move.captured
        elif move.captured is not None:
            self.grid[er][ec] = move.captured
        if move.is_castling:
            rr_s, rc_s = move.rook_start
            rr_e, rc_e = move.rook_end
            rook = self.grid[rr_e][rc_e]
            self.grid[rr_s][rc_s] = rook
            rook.has_moved = move.prev_rook_has_moved
            self.grid[rr_e][rc_e] = None
        self.en_passant_target = move.prev_en_passant_target