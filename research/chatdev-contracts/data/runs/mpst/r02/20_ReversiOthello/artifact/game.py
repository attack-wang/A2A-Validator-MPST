'''
game.py
Game-flow controller for Reversi (Othello).
The Game class wraps a Board and manages:
    * whose turn it is (Black always starts),
    * executing moves and remembering what was flipped,
    * automatic passing when a player has no legal move,
    * detecting the end of the game (board full or neither player can move),
    * deciding the winner from the final disc counts.
'''
from board import Board, BLACK, WHITE
class Game:
    '''Controls the state and flow of a single Reversi match.'''
    def __init__(self):
        '''Start a new match on a fresh board; Black moves first.'''
        self.board = Board()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None          # BLACK, WHITE, or None for a tie
        self.last_move = None       # (row, col) of the most recent placement
        self.last_flipped = []      # discs flipped by the most recent placement
        self.passed_player = None   # player who was forced to pass, if any
    def make_move(self, row, col):
        '''
        Attempt to place the current player's disc on (row, col).
        Returns True when the move is legal and has been executed; the turn
        then advances automatically (including automatic passes). Returns
        False when the move is illegal or the game is already over.
        '''
        if self.game_over:
            return False
        flipped = self.board.place_disc(row, col, self.current_player)
        if flipped is None:
            return False
        self.last_move = (row, col)
        self.last_flipped = flipped
        self._advance_turn()
        return True
    def _advance_turn(self):
        '''
        Hand the turn to the other player, applying automatic passes.
        If the opponent cannot move but the current player still can, the
        opponent passes and the current player plays again. If neither
        player can move (or the board is full) the game ends.
        '''
        opponent = WHITE if self.current_player == BLACK else BLACK
        # End of game: the board is completely filled.
        if self.board.is_full():
            self.game_over = True
            self.passed_player = None
            self._determine_winner()
            return
        if self.board.has_valid_move(opponent):
            # Normal turn swap.
            self.current_player = opponent
            self.passed_player = None
        elif self.board.has_valid_move(self.current_player):
            # The opponent is stuck: they pass, current player moves again.
            self.passed_player = opponent
        else:
            # Neither side can move: the game is over.
            self.game_over = True
            self.passed_player = None
            self._determine_winner()
    def _determine_winner(self):
        '''Decide the winner from the final disc counts (None means a tie).'''
        black, white = self.board.get_score()
        if black > white:
            self.winner = BLACK
        elif white > black:
            self.winner = WHITE
        else:
            self.winner = None
    def is_game_over(self):
        '''Return True once the match has finished.'''
        return self.game_over
    def get_valid_moves(self):
        '''Return the legal moves for the player who is on turn.'''
        if self.game_over:
            return []
        return self.board.get_valid_moves(self.current_player)
    def get_score(self):
        '''Return the live score as a tuple (black_discs, white_discs).'''
        return self.board.get_score()