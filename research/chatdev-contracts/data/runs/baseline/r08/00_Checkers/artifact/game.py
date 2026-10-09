from piece import Piece
from board import Board
from move import Move
class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = 'R'  # Red moves first
        self.game_over = False
        self.winner = None
        self.chain_piece = None  # (row, col) of piece that must continue jumping
    def get_all_moves(self, color):
        """Return all legal moves for the given color, enforcing mandatory capture."""
        moves = []
        captures = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    for mv in self.piece_moves(row, col):
                        if mv.is_capture():
                            captures.append(mv)
                        else:
                            moves.append(mv)
        if captures:
            return captures
        return moves
    def piece_moves(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece is None:
            return []
        moves = []
        for dr, dc in piece.get_directions():
            r1, c1 = row + dr, col + dc
            r2, c2 = row + 2 * dr, col + 2 * dc
            if self.board.is_inside(r1, c1) and self.board.is_playable(r1, c1):
                target = self.board.get_piece(r1, c1)
                if target is None:
                    moves.append(Move(row, col, r1, c1, None))
                elif target.color != piece.color and self.board.is_inside(r2, c2) \
                        and self.board.is_playable(r2, c2) \
                        and self.board.get_piece(r2, c2) is None:
                    moves.append(Move(row, col, r2, c2, (r1, c1)))
        return moves
    def is_legal_move(self, move):
        if not self.board.is_inside(move.from_row, move.from_col):
            return False
        piece = self.board.get_piece(move.from_row, move.from_col)
        if piece is None or piece.color != self.current_player:
            return False
        if self.chain_piece is not None and (move.from_row, move.from_col) != self.chain_piece:
            return False
        legal = self.get_all_moves(self.current_player)
        return move in legal
    def apply_move(self, move):
        piece = self.board.get_piece(move.from_row, move.from_col)
        self.board.remove_piece(move.from_row, move.from_col)
        if move.is_capture():
            cap_row, cap_col = move.captured
            self.board.remove_piece(cap_row, cap_col)
        self.board.grid[move.to_row][move.to_col] = piece
        # Kinging
        if not piece.is_king:
            if piece.color == 'R' and move.to_row == 0:
                piece.crown()
            elif piece.color == 'B' and move.to_row == 7:
                piece.crown()
        # Chain jumps
        if move.is_capture():
            further = [m for m in self.piece_moves(move.to_row, move.to_col) if m.is_capture()]
            if further:
                self.chain_piece = (move.to_row, move.to_col)
                return True  # must continue jumping
        self.chain_piece = None
        self.switch_turn()
        return False
    def switch_turn(self):
        self.current_player = 'B' if self.current_player == 'R' else 'R'
        self.check_game_over()
    def check_game_over(self):
        if self.chain_piece is not None:
            return
        moves = self.get_all_moves(self.current_player)
        if not moves:
            self.game_over = True
            self.winner = 'B' if self.current_player == 'R' else 'R'
        # also check if opponent has no pieces? Actually if current player has no moves, current loses.
        # But what if current player has moves but opponent has no pieces? That can't happen because
        # opponent just moved... Actually opponent could have all pieces captured during chain jumps.
        # Hmm, chain jumps: if during chain the opponent loses all pieces, the chain piece may still
        # have further jumps. Let's handle: if opponent has no pieces, game over.
        opponent = 'B' if self.current_player == 'R' else 'R'
        opp_count = self.count_pieces(opponent)
        if opp_count == 0:
            self.game_over = True
            self.winner = self.current_player
    def count_pieces(self, color):
        count = 0
        for row in range(8):
            for col in range(8):
                p = self.board.get_piece(row, col)
                if p and p.color == color:
                    count += 1
        return count
    def resign(self, color):
        self.game_over = True
        self.winner = 'B' if color == 'R' else 'R'