'''
game.py
Defines the Game class which orchestrates the flow of a Gomoku match:
turn alternation, move application, and win/draw detection.
'''
from board import Board
from player import Player
from constants import BLACK, WHITE
class Game:
    '''Manages the state and rules of a Gomoku game.'''
    def __init__(self, board=None, player_black=None, player_white=None):
        self.board = board if board is not None else Board()
        self.players = {
            BLACK: player_black if player_black else Player('Black', BLACK),
            WHITE: player_white if player_white else Player('White', WHITE),
        }
        self.current_color = BLACK  # black moves first
        self.winner_color = None
        self.game_over = False
        self.winning_line = None
        self.last_move = None
        self.move_count = 0
    @property
    def current_player(self):
        return self.players[self.current_color]
    def play_turn(self, row, col):
        '''Attempt to place the current player's stone at (row, col).
        Returns True if the move was applied, False otherwise.'''
        if self.game_over:
            return False
        if not self.board.place_stone(row, col, self.current_color):
            return False
        self.last_move = (row, col)
        self.move_count += 1
        if self.board.check_win(row, col):
            self.game_over = True
            self.winner_color = self.current_color
            self.winning_line = self.board.get_winning_line(row, col)
        elif self.board.is_full():
            self.game_over = True
            self.winner_color = None  # draw
        else:
            self.current_color = WHITE if self.current_color == BLACK else BLACK
        return True
    def reset(self):
        self.board.reset()
        self.current_color = BLACK
        self.winner_color = None
        self.game_over = False
        self.winning_line = None
        self.last_move = None
        self.move_count = 0