'''
game.py
Defines the Game class: the controller that owns the Board, alternates
turns between Black and White, detects wins/draws and produces the
status message shown in the GUI.
'''
from constants import (
    BLACK, WHITE, PLAYER_NAMES, ONGOING, BLACK_WINS, WHITE_WINS, DRAW,
)
from board import Board
class Game:
    '''
    Game controller: holds the Board, the current player, the last move,
    the winning line and the overall game state. The GUI interacts only
    with this class.
    '''
    def __init__(self):
        '''Start a fresh match with Black moving first.'''
        self.board = Board()
        self.current_player = BLACK
        self.state = ONGOING
        self.last_move = None
        self.winning_line = None
    def reset(self):
        '''Clear the board and restore the initial state (Black first).'''
        self.board.reset()
        self.current_player = BLACK
        self.state = ONGOING
        self.last_move = None
        self.winning_line = None
    def make_move(self, row, col):
        '''
        Place a stone for the current player at (row, col).
        Return True when the move was applied, False when the game is
        over or the cell is invalid. Updates win/draw state and switches
        the turn while the game is still ongoing.
        '''
        if self.state != ONGOING:
            return False
        if not self.board.place_stone(row, col, self.current_player):
            return False
        self.last_move = (row, col)
        self.winning_line = self.board.get_winning_line(
            row, col, self.current_player)
        if self.winning_line:
            self.state = (BLACK_WINS if self.current_player == BLACK
                          else WHITE_WINS)
        elif self.board.is_full():
            self.state = DRAW
        else:
            self.current_player = (WHITE if self.current_player == BLACK
                                   else BLACK)
        return True
    def get_status_message(self):
        '''Return the human-readable text displayed in the status bar.'''
        if self.state == BLACK_WINS:
            return "Black wins! Click Restart to play again."
        if self.state == WHITE_WINS:
            return "White wins! Click Restart to play again."
        if self.state == DRAW:
            return "Draw - the board is full. Click Restart to play again."
        return f"{PLAYER_NAMES[self.current_player]}'s turn"