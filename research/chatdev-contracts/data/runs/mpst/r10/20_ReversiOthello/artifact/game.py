'''
game.py
Turn-management and rule orchestration for the Reversi (Othello) game.
The Game class wraps the Board, tracks whose turn it is, validates and
applies moves, automatically skips a player who has no valid move, and
detects the end of the game (board full or neither player able to move).
'''
from constants import BLACK, WHITE, PLAYER_NAMES
from board import Board
class Game:
    '''Coordinates board state, turn order, messages and game-over detection.'''
    def __init__(self):
        '''Create the board; Black always moves first in Othello.'''
        self.board = Board()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None
        self.message = "Black moves first - click a yellow dot"
        self.last_move = None
        self.last_flipped = []
    def get_valid_moves(self):
        '''Return all (row, col) valid moves for the current player.'''
        return self.board.get_valid_moves(self.current_player)
    def get_score(self):
        '''Return current disc counts as {BLACK: n, WHITE: n}.'''
        return self.board.get_score()
    def make_move(self, row, col):
        '''Attempt to place the current player's disc at (row, col).
        Returns True on success; on failure sets an error message and
        returns False without changing state.
        '''
        if self.game_over:
            return False
        flipped = self.board.place_disc(row, col, self.current_player)
        if flipped is None:
            self.message = "Invalid move - choose a highlighted cell"
            return False
        self.last_flipped = flipped
        self.last_move = (row, col)
        mover_name = PLAYER_NAMES[self.current_player]
        flip_text = (f"{mover_name} played ({chr(ord('A') + col)}{row + 1}) and flipped "
                     f"{len(flipped)} disc{'s' if len(flipped) != 1 else ''}")
        self._advance_turn(flip_text)
        return True
    def _advance_turn(self, message):
        '''Hand the turn to the opponent, skipping them if they have no
        valid move, and end the game when neither player can move
        (which also covers a full board).'''
        next_player = self.board.opponent(self.current_player)
        if self.board.has_valid_move(next_player):
            self.current_player = next_player
            self.message = f"{message}. {PLAYER_NAMES[next_player]}'s turn"
        elif self.board.has_valid_move(self.current_player):
            self.message = (f"{message}. {PLAYER_NAMES[next_player]} has no valid "
                            f"move and passes - {PLAYER_NAMES[self.current_player]} moves again")
        else:
            self.message = message
            self._end_game()
    def _end_game(self):
        '''Mark the game finished and determine the winner by disc count.'''
        self.game_over = True
        score = self.board.get_score()
        if score[BLACK] > score[WHITE]:
            self.winner = BLACK
        elif score[WHITE] > score[BLACK]:
            self.winner = WHITE
        else:
            self.winner = None
    def reset(self):
        '''Restore the initial state for a brand-new match.'''
        self.board.reset()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None
        self.message = "New game - Black moves first"
        self.last_move = None
        self.last_flipped = []