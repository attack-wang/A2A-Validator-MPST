'''
Game module for the Gomoku game.
Provides the Game class, which owns the Board and drives the match flow:
whose turn it is, applying moves, detecting wins/draws and restarting.
'''
from enum import Enum
from config import BLACK, WHITE, PLAYER_NAMES
from board import Board
class GameState(Enum):
    '''All possible states of a running Gomoku match.'''
    ONGOING = "Ongoing"
    BLACK_WINS = "Black wins"
    WHITE_WINS = "White wins"
    DRAW = "Draw"
class Game:
    '''Controls the Gomoku match: turn order, move handling and end-game detection.'''
    def __init__(self):
        '''Create a fresh game; Black always takes the first move.'''
        self.board = Board()
        self.current_player = BLACK
        self.state = GameState.ONGOING
        self.winning_line = []      # Board positions of the winning stones
    def handle_move(self, row, col):
        '''Apply the current player's move at (row, col).
        Places the stone, then checks for a win or a draw and either
        switches turns or records the final state.
        Returns True if the move was accepted, False otherwise.'''
        if self.state != GameState.ONGOING:
            return False
        if not self.board.place_stone(row, col, self.current_player):
            return False
        winning_line = self.board.check_win(row, col, self.current_player)
        if winning_line:
            self.winning_line = winning_line
            self.state = (GameState.BLACK_WINS if self.current_player == BLACK
                          else GameState.WHITE_WINS)
        elif self.board.is_full():
            self.state = GameState.DRAW
        else:
            self.switch_player()
        return True
    def switch_player(self):
        '''Hand the turn over to the other player.'''
        self.current_player = WHITE if self.current_player == BLACK else BLACK
    def get_current_player_name(self):
        '''Return the display name of the player who moves next.'''
        return PLAYER_NAMES[self.current_player]
    def get_state_message(self):
        '''Return a human-readable description of the current game state.'''
        if self.state == GameState.ONGOING:
            return "{} player's turn".format(self.get_current_player_name())
        if self.state == GameState.BLACK_WINS:
            return "Black wins - five in a row!"
        if self.state == GameState.WHITE_WINS:
            return "White wins - five in a row!"
        return "It's a draw - the board is full."
    def restart(self):
        '''Reset the board, the turn order and the game state.'''
        self.board.reset()
        self.current_player = BLACK
        self.state = GameState.ONGOING
        self.winning_line = []