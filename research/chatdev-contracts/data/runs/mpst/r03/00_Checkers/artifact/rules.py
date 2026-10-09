'''
rules.py
Rules engine: generates legal moves, validates jumps, enforces
forced captures and kinging.
Internal coordinates: (row, col), row 0 at top. Red moves up (toward
row 0) and kings on row 0; Black moves down (toward row 7) and kings
on row 7. Standard rules: if any capture is available, the player MUST
capture; men jump only forward, kings jump in all four directions.
'''
from pieces import RED, BLACK
from board import Board
class Rules:
    FORWARD = {RED: -1, BLACK: +1}   # red moves up (toward row 0), black moves down
    ALL_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    @staticmethod
    def get_forward_dirs(color):
        dr = Rules.FORWARD[color]
        return [(dr, -1), (dr, 1)]
    @staticmethod
    def get_dirs_for_piece(piece):
        return Rules.ALL_DIRS if piece.is_king else Rules.get_forward_dirs(piece.color)
    @staticmethod
    def get_jump_target(board, from_pos, to_pos, color):
        '''Return position of captured piece if from->to is a legal jump, else None.'''
        fr, fc = from_pos
        tr, tc = to_pos
        dr, dc = tr - fr, tc - fc
        if abs(dr) != 2 or abs(dc) != 2:
            return None
        if not Board.in_bounds(tr, tc):          # bounds check FIRST (bug fix)
            return None
        piece = board.get_piece(fr, fc)
        if piece is None or piece.color != color:
            return None
        if not piece.is_king:
            # man can only jump forward
            if dr != Rules.FORWARD[color]:
                return None
        mr, mc = fr + dr // 2, fc + dc // 2
        if not Board.in_bounds(mr, mc):          # middle square must be on board
            return None
        middle = board.get_piece(mr, mc)
        if middle is None or middle.color == color:
            return None
        if board.get_piece(tr, tc) is not None:
            return None
        return (mr, mc)
    @staticmethod
    def get_captures_for_piece(board, pos):
        '''All single-jump landing squares for the piece at pos.'''
        piece = board.get_piece(*pos)
        if piece is None:
            return []
        captures = []
        for dr, dc in Rules.get_dirs_for_piece(piece):
            to = (pos[0] + 2 * dr, pos[1] + 2 * dc)
            if Rules.get_jump_target(board, pos, to, piece.color) is not None:
                captures.append(to)
        return captures
    @staticmethod
    def get_all_captures(board, color):
        '''dict: piece position -> list of landing positions (only if non-empty).'''
        captures = {}
        for r in range(Board.BOARD_SIZE):
            for c in range(Board.BOARD_SIZE):
                piece = board.get_piece(r, c)
                if piece is not None and piece.color == color:
                    landings = Rules.get_captures_for_piece(board, (r, c))
                    if landings:
                        captures[(r, c)] = landings
        return captures
    @staticmethod
    def get_simple_moves_for_piece(board, pos):
        piece = board.get_piece(*pos)
        if piece is None:
            return []
        moves = []
        for dr, dc in Rules.get_dirs_for_piece(piece):
            tr, tc = pos[0] + dr, pos[1] + dc
            if Board.in_bounds(tr, tc) and board.get_piece(tr, tc) is None:
                moves.append((tr, tc))
        return moves
    @staticmethod
    def get_all_simple_moves(board, color):
        moves = {}
        for r in range(Board.BOARD_SIZE):
            for c in range(Board.BOARD_SIZE):
                piece = board.get_piece(r, c)
                if piece is not None and piece.color == color:
                    dests = Rules.get_simple_moves_for_piece(board, (r, c))
                    if dests:
                        moves[(r, c)] = dests
        return moves
    @staticmethod
    def get_legal_moves(board, color):
        captures = Rules.get_all_captures(board, color)
        if captures:
            return captures, True
        return Rules.get_all_simple_moves(board, color), False
    @staticmethod
    def get_king_row(color):
        return 0 if color == RED else 7  # red kings at top (row 0), black at bottom (row 7)