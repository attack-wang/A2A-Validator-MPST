'''
game_logic.py
Pure game rules for Reversi (Othello): the Board class handles disc placement,
direction scanning, disc flipping and scoring; the Game class manages turns,
passes and game-over detection.
'''
from constants import (EMPTY, BLACK, WHITE, BOARD_SIZE, PLAYER_NAMES)
class Board:
    """
    8x8 Reversi board with full rule implementation:
      * valid-move detection in all eight directions,
      * disc flipping,
      * score counting,
      * game-over detection.
    """
    DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1),  (1, 0),  (1, 1)]
    def __init__(self):
        self.size = BOARD_SIZE
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self._setup_initial_position()
    def _setup_initial_position(self):
        """Place the four starting discs in the centre."""
        mid = self.size // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid][mid] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
    def in_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size
    def get_discs_to_flip(self, row, col, player):
        """
        Return the list of opponent discs that would be flipped if `player`
        placed a disc at (row, col). Empty list means the move is invalid.
        """
        if not self.in_bounds(row, col) or self.grid[row][col] != EMPTY:
            return []
        if player not in (BLACK, WHITE):
            return []
        opponent = WHITE if player == BLACK else BLACK
        flipped = []
        for dr, dc in self.DIRECTIONS:
            line = []
            r, c = row + dr, col + dc
            # Walk over contiguous opponent discs.
            while self.in_bounds(r, c) and self.grid[r][c] == opponent:
                line.append((r, c))
                r += dr
                c += dc
            # A friendly disc must close the line with at least one flip.
            if line and self.in_bounds(r, c) and self.grid[r][c] == player:
                flipped.extend(line)
        return flipped
    def is_valid_move(self, row, col, player):
        return len(self.get_discs_to_flip(row, col, player)) > 0
    def make_move(self, row, col, player):
        """Place a disc, flip captured discs, return the flipped positions."""
        flipped = self.get_discs_to_flip(row, col, player)
        if not flipped:
            return []
        self.grid[row][col] = player
        for r, c in flipped:
            self.grid[r][c] = player
        return flipped
    def get_valid_moves(self, player):
        """All legal (row, col) moves for `player`."""
        return [(r, c)
                for r in range(self.size)
                for c in range(self.size)
                if self.is_valid_move(r, c, player)]
    def has_valid_moves(self, player):
        return len(self.get_valid_moves(player)) > 0
    def get_score(self):
        """Return {BLACK: n_black, WHITE: n_white}."""
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return {BLACK: black, WHITE: white}
    def is_full(self):
        return all(cell != EMPTY for row in self.grid for cell in row)
    def is_game_over(self):
        """Game over when the board is full or neither side can move."""
        if self.is_full():
            return True
        return not (self.has_valid_moves(BLACK) or self.has_valid_moves(WHITE))
class Game:
    """
    Turn-based game manager on top of Board:
      * alternates players,
      * automatically passes a player with no legal moves,
      * detects game over and the winner,
      * remembers the last move for the GUI.
    """
    def __init__(self):
        self.board = Board()
        self.current_player = BLACK          # black always moves first
        self.game_over = False
        self.winner = None                   # BLACK, WHITE or None (draw)
        self.last_move = None                # (row, col) of last placement
        self.pass_message = None             # text shown when a player passes
    def try_move(self, row, col):
        """
        Attempt to place the current player's disc at (row, col).
        Returns the list of flipped positions on success, otherwise None.
        """
        if self.game_over:
            return None
        if not self.board.is_valid_move(row, col, self.current_player):
            return None
        flipped = self.board.make_move(row, col, self.current_player)
        self.last_move = (row, col)
        self.pass_message = None
        self._advance_turn()
        return flipped
    def _advance_turn(self):
        """Hand the turn over, handling passes and game-over detection."""
        if self.board.is_game_over():
            self.game_over = True
            self._determine_winner()
            return
        opponent = WHITE if self.current_player == BLACK else BLACK
        if self.board.has_valid_moves(opponent):
            self.current_player = opponent
        else:
            # Opponent cannot move: they pass, current player plays again.
            self.pass_message = (f"{PLAYER_NAMES[opponent]} has no valid move "
                                 f"— turn passes!")
    def _determine_winner(self):
        score = self.board.get_score()
        if score[BLACK] > score[WHITE]:
            self.winner = BLACK
        elif score[WHITE] > score[BLACK]:
            self.winner = WHITE
        else:
            self.winner = None
    def get_valid_moves(self):
        """Legal moves for the player whose turn it is."""
        if self.game_over:
            return []
        return self.board.get_valid_moves(self.current_player)
    def restart(self):
        """Reset the game to the initial position."""
        self.board = Board()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.pass_message = None