'''
Core game logic for Reversi (Othello).
This module implements the rules of Reversi on an 8x8 board:
- Valid move detection (a move must flip at least one opponent disc)
- Automatic flipping of opponent discs in all 8 directions
- Turn management with automatic passing when a player has no moves
- Score tracking and game-over / winner determination
'''
class ReversiGame:
    '''Represents the full state and rules of a Reversi (Othello) game.'''
    BOARD_SIZE = 8
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    # The 8 directions: horizontal, vertical, and diagonal
    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]
    def __init__(self):
        '''Create an 8x8 board with the standard central starting position.'''
        self.board = [[self.EMPTY for _ in range(self.BOARD_SIZE)]
                      for _ in range(self.BOARD_SIZE)]
        mid = self.BOARD_SIZE // 2
        self.board[mid - 1][mid - 1] = self.WHITE
        self.board[mid][mid] = self.WHITE
        self.board[mid - 1][mid] = self.BLACK
        self.board[mid][mid - 1] = self.BLACK
        self.current_player = self.BLACK  # Black always moves first
    # ------------------------------------------------------------------
    # Basic helpers
    # ------------------------------------------------------------------
    def get_opponent(self, player):
        '''Return the opponent's color for the given player color.'''
        return self.WHITE if player == self.BLACK else self.BLACK
    def in_bounds(self, row, col):
        '''Return True if (row, col) lies inside the 8x8 board.'''
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE
    # ------------------------------------------------------------------
    # Move rules
    # ------------------------------------------------------------------
    def get_flippable_discs(self, row, col, player):
        '''
        Return the list of (row, col) opponent disc positions that would be
        flipped if `player` placed a disc on the empty cell (row, col).
        Returns an empty list when the move is not legal.
        '''
        if not self.in_bounds(row, col) or self.board[row][col] != self.EMPTY:
            return []
        opponent = self.get_opponent(player)
        flippable = []
        for dr, dc in self.DIRECTIONS:
            line = []
            r, c = row + dr, col + dc
            # Collect the run of consecutive opponent discs in this direction
            while self.in_bounds(r, c) and self.board[r][c] == opponent:
                line.append((r, c))
                r += dr
                c += dc
            # The run is capturable only if it is terminated by our own disc
            if line and self.in_bounds(r, c) and self.board[r][c] == player:
                flippable.extend(line)
        return flippable
    def is_valid_move(self, row, col, player):
        '''Return True if `player` may legally place a disc at (row, col).'''
        return len(self.get_flippable_discs(row, col, player)) > 0
    def get_valid_moves(self, player):
        '''Return a list of every legal (row, col) move for `player`.'''
        return [
            (row, col)
            for row in range(self.BOARD_SIZE)
            for col in range(self.BOARD_SIZE)
            if self.board[row][col] == self.EMPTY
            and self.is_valid_move(row, col, player)
        ]
    # ------------------------------------------------------------------
    # Playing moves
    # ------------------------------------------------------------------
    def make_move(self, row, col, player):
        '''
        Place a disc for `player` at (row, col), flip every flippable
        opponent disc, then advance the turn. Returns False for illegal
        moves (nothing is changed in that case).
        '''
        flippable = self.get_flippable_discs(row, col, player)
        if not flippable:
            return False
        self.board[row][col] = player
        for r, c in flippable:
            self.board[r][c] = player
        self._advance_turn()
        return True
    def _advance_turn(self):
        '''
        Hand the turn to the opponent. If the opponent has no legal move
        they must pass, so the current player keeps playing. If neither
        side can move the game is over (handled by is_game_over()).
        '''
        opponent = self.get_opponent(self.current_player)
        if self.get_valid_moves(opponent):
            self.current_player = opponent
    # ------------------------------------------------------------------
    # Score and game state
    # ------------------------------------------------------------------
    def get_score(self):
        '''Return a dict mapping each player color to its disc count.'''
        black = sum(row.count(self.BLACK) for row in self.board)
        white = sum(row.count(self.WHITE) for row in self.board)
        return {self.BLACK: black, self.WHITE: white}
    def is_board_full(self):
        '''Return True when no empty cells remain on the board.'''
        return all(cell != self.EMPTY for row in self.board for cell in row)
    def is_game_over(self):
        '''The game ends when the board is full or neither player can move.'''
        if self.is_board_full():
            return True
        return (not self.get_valid_moves(self.BLACK)
                and not self.get_valid_moves(self.WHITE))
    def get_winner(self):
        '''
        Return the color of the winning player, or None when the game is
        still in progress or ends in a tie.
        '''
        if not self.is_game_over():
            return None
        score = self.get_score()
        if score[self.BLACK] > score[self.WHITE]:
            return self.BLACK
        if score[self.WHITE] > score[self.BLACK]:
            return self.WHITE
        return None