'''
CheckersGame class: rules, legal-move generation, move application,
mandatory captures, multi-jump continuation, kinging and win detection.
'''
from constants import (BOARD_SIZE, CROWN_ROW, FORWARD_DIRECTIONS,
                       KING_DIRECTIONS, RED, BLACK)
from board import Board
class IllegalMoveError(Exception):
    """Raised when a requested move violates the rules."""
def square_name(pos):
    """(row, col) -> algebraic name such as 'b6'."""
    row, col = pos
    return f"{'abcdefgh'[col]}{BOARD_SIZE - row}"
class CheckersGame:
    """State and rules of one checkers game."""
    def __init__(self, starting_player=RED):
        self.board = Board()
        self.current_player = starting_player
        self.continuation_from = None  # square the same player must keep jumping from
    # ------------------------------------------------------------------ helpers
    @staticmethod
    def opponent(color):
        return BLACK if color == RED else RED
    def _pieces_of(self, color):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board.get_piece(row, col)
                if piece is not None and piece.color == color:
                    yield (row, col), piece
    def _directions_for(self, piece):
        if piece.is_king:
            return KING_DIRECTIONS
        return FORWARD_DIRECTIONS[piece.color]
    # --------------------------------------------------------- move generation
    def get_piece_moves(self, pos):
        """One-step destinations for the piece at pos: {dest: captured_or_None}."""
        row, col = pos
        piece = self.board.get_piece(row, col)
        if piece is None:
            return {}
        moves = {}
        for dr, dc in self._directions_for(piece):
            adj_row, adj_col = row + dr, col + dc
            if not self.board.in_bounds(adj_row, adj_col):
                continue
            adjacent = self.board.get_piece(adj_row, adj_col)
            if adjacent is None:
                moves[(adj_row, adj_col)] = None          # simple move
            elif adjacent.color != piece.color:
                land_row, land_col = row + 2 * dr, col + 2 * dc
                if (self.board.in_bounds(land_row, land_col)
                        and self.board.get_piece(land_row, land_col) is None):
                    moves[(land_row, land_col)] = (adj_row, adj_col)  # jump
        return moves
    def has_any_capture(self, color):
        """True if `color` has at least one jump available right now."""
        for pos, _piece in self._pieces_of(color):
            if any(captured is not None
                   for captured in self.get_piece_moves(pos).values()):
                return True
        return False
    def has_any_move(self, color):
        """True if `color` can make at least one legal move right now."""
        if self.has_any_capture(color):
            return True
        for pos, _piece in self._pieces_of(color):
            if any(captured is None
                   for captured in self.get_piece_moves(pos).values()):
                return True
        return False
    def get_all_moves(self, color):
        """All legal moves for `color` as full paths [(from, ..., to), ...].
        When any capture is available, only capture chains are returned
        because captures are compulsory.
        """
        moves = []
        if self.has_any_capture(color):
            for pos, _piece in self._pieces_of(color):
                moves.extend(self._capture_chains_from(pos))
            return moves
        for pos, _piece in self._pieces_of(color):
            for dest, captured in self.get_piece_moves(pos).items():
                if captured is None:
                    moves.append([pos, dest])
        return moves
    def _capture_chains_from(self, start):
        """All complete jump chains starting from `start` (board is restored)."""
        chains = []
        piece = self.board.get_piece(*start)
        if piece is None:
            return chains
        def dfs(pos, path, captured):
            extended = False
            for dest, cap in self.get_piece_moves(pos).items():
                if cap is None or cap in captured:
                    continue
                jumped_piece = self.board.get_piece(*cap)
                # simulate the jump
                self.board.remove_piece(*pos)
                self.board.remove_piece(*cap)
                self.board.place_piece(piece, *dest)
                dfs(dest, path + [dest], captured | {cap})
                # undo the simulation
                self.board.remove_piece(*dest)
                self.board.place_piece(jumped_piece, *cap)
                self.board.place_piece(piece, *pos)
                extended = True
            if not extended and len(path) > 1:
                chains.append(list(path))
        dfs(start, [start], set())
        return chains
    # -------------------------------------------------------------- applying
    def apply_move(self, path):
        """Apply a move given as a list of positions (chain). Returns info dict."""
        if len(path) < 2:
            raise IllegalMoveError(
                "A move needs a 'from' square and a 'to' square, e.g. b6-d8.")
        start = path[0]
        if self.continuation_from is not None and start != self.continuation_from:
            raise IllegalMoveError(
                f"You must keep jumping with the piece on "
                f"{square_name(self.continuation_from)}.")
        piece = self.board.get_piece(*start)
        if piece is None:
            raise IllegalMoveError(f"There is no piece on {square_name(start)}.")
        if piece.color != self.current_player:
            raise IllegalMoveError("That piece belongs to your opponent.")
        must_capture = (self.continuation_from is not None
                        or self.has_any_capture(self.current_player))
        captured_positions = []
        current = start
        for dest in path[1:]:
            steps = self.get_piece_moves(current)
            if dest not in steps:
                raise IllegalMoveError(
                    f"Illegal step {square_name(current)}-{square_name(dest)}; "
                    f"type 'moves' to list your legal moves.")
            captured = steps[dest]
            if captured is None:
                if must_capture:
                    raise IllegalMoveError(
                        "Captures are compulsory: you must jump when a jump "
                        "is available.")
                if len(path) != 2:
                    raise IllegalMoveError(
                        "Only jumps may be chained; a simple move is one step.")
            else:
                if captured in captured_positions:
                    raise IllegalMoveError(
                        "The same piece cannot be captured twice in one turn.")
                self.board.remove_piece(*captured)
                captured_positions.append(captured)
            self.board.move_piece(current, dest)
            current = dest
        crowned = False
        if not piece.is_king and current[0] == CROWN_ROW[piece.color]:
            piece.crown()
            crowned = True
        more_jumps = (not crowned and any(
            captured is not None
            for captured in self.get_piece_moves(current).values()))
        if more_jumps:
            self.continuation_from = current
        else:
            self.continuation_from = None
            self.current_player = self.opponent(self.current_player)
        return {
            "captured": captured_positions,
            "crowned": crowned,
            "continue_from": self.continuation_from,
        }
    # ------------------------------------------------------------- game state
    def is_game_over(self):
        return (self.board.count_pieces(RED) == 0
                or self.board.count_pieces(BLACK) == 0
                or not self.has_any_move(self.current_player))
    def get_winner(self):
        if self.board.count_pieces(RED) == 0:
            return BLACK
        if self.board.count_pieces(BLACK) == 0:
            return RED
        if not self.has_any_move(self.current_player):
            return self.opponent(self.current_player)
        return None