'''
game.py
Turn management and high-level game state for Reversi.
Wraps the pure-logic Board with the rules that govern whose turn it is,
when a player must pass, and when the game has ended.
'''
from board import Board, BLACK, WHITE, EMPTY
class GameController:
    '''Coordinates turns, pass handling, scoring and game-over detection.'''
    def __init__(self):
        '''Create a fresh board and set Black as the starting player.'''
        self.board = Board()
        self.current_player = BLACK  # black always moves first
        self.game_over = False
        self.winner = None  # BLACK, WHITE, or EMPTY (0) for a tie
        self.last_move = None  # (row, col) of most recent placement
        self.skipped_player = None  # player who had to pass this turn
    def make_move(self, row, col):
        '''Attempt to place the current player's disc at (row, col).
        Returns the list of flipped positions on success, or None when the
        move is illegal or the game is already over.
        '''
        if self.game_over:
            return None
        flipped = self.board.place_disc(row, col, self.current_player)
        if flipped is None:
            return None
        self.last_move = (row, col)
        self._advance_turn()
        return flipped
    def _advance_turn(self):
        '''Hand the turn to the opponent, forcing a pass or ending the game.
        If the opponent has a legal move they play next; otherwise, if the
        current player still has a move, the opponent passes and the current
        player keeps the turn; if neither can move the game is over.
        '''
        self.skipped_player = None
        opponent = WHITE if self.current_player == BLACK else BLACK
        if self.board.get_valid_moves(opponent):
            self.current_player = opponent
        elif self.board.get_valid_moves(self.current_player):
            self.skipped_player = opponent
        else:
            self.game_over = True
            self._determine_winner()
    def _determine_winner(self):
        '''Set self.winner based on the current disc counts.'''
        black, white = self.board.count_discs()
        if black > white:
            self.winner = BLACK
        elif white > black:
            self.winner = WHITE
        else:
            self.winner = EMPTY  # tie
    def get_scores(self):
        '''Return a (black, white) tuple with the current disc counts.'''
        return self.board.count_discs()
    def has_valid_move(self, player=None):
        '''Return True if the given (or current) player has a legal move.'''
        if player is None:
            player = self.current_player
        return bool(self.board.get_valid_moves(player))
    def reset(self):
        '''Restore the initial game state for a new match.'''
        self.board.reset()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.skipped_player = None