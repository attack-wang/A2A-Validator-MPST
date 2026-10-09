'''
Game module: manages the flow of a Reversi match — turn order, move
execution, pass handling, and game-over detection.
'''
from constants import BLACK, WHITE, PLAYER_NAMES
from board import Board
class Game:
    '''
    Controls the state and progression of a Reversi game.
    '''
    def __init__(self):
        '''Initialize a new game with the standard starting position.'''
        self.board = Board()
        self.current_player = BLACK  # Black always moves first
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.message = ""  # informational message for the GUI
    def make_move(self, row, col):
        '''
        Attempt to place a disc for the current player at (row, col).
        Returns True if the move was legal and applied, else False.
        '''
        if self.game_over:
            return False
        flipped = self.board.place_disc(row, col, self.current_player)
        if flipped == 0:
            self.message = "Invalid move!"
            return False
        self.last_move = (row, col)
        self.message = ""
        self._advance_turn()
        return True
    def _advance_turn(self):
        '''
        Pass the turn to the other player. If the next player has no valid
        moves, they are skipped; if neither player can move, the game ends.
        '''
        opponent = self.board.get_opponent(self.current_player)
        if self.board.get_valid_moves(opponent):
            self.current_player = opponent
        elif self.board.get_valid_moves(self.current_player):
            # Opponent must pass; current player moves again
            self.message = f"{PLAYER_NAMES[opponent]} has no valid moves and must pass!"
            # current_player stays the same
        else:
            # Neither player can move — game over
            self.game_over = True
            self._determine_winner()
    def _determine_winner(self):
        '''Set the winner based on the final disc counts.'''
        black_score, white_score = self.board.get_score()
        if black_score > white_score:
            self.winner = BLACK
        elif white_score > black_score:
            self.winner = WHITE
        else:
            self.winner = None  # draw
    def check_game_over(self):
        '''
        Check whether the game has ended: the board is full, or neither
        player has any valid moves remaining.
        '''
        if self.game_over:
            return True
        if self.board.is_full():
            self.game_over = True
            self._determine_winner()
            return True
        if not self.board.get_valid_moves(BLACK) and not self.board.get_valid_moves(WHITE):
            self.game_over = True
            self._determine_winner()
            return True
        return False
    def has_valid_move(self, player):
        '''Return True if `player` has at least one valid move.'''
        return len(self.board.get_valid_moves(player)) > 0
    def get_valid_moves(self):
        '''Return the valid moves for the current player.'''
        return self.board.get_valid_moves(self.current_player)
    def get_score(self):
        '''Return a tuple (black_score, white_score).'''
        return self.board.get_score()
    def get_current_player_name(self):
        '''Return the display name of the current player.'''
        return PLAYER_NAMES[self.current_player]