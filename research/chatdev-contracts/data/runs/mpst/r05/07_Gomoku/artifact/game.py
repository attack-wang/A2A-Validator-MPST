'''
game.py
Game controller: manages turns, moves, and overall game state.
'''
from config import BLACK, WHITE, PLAYER_NAMES
from board import Board
class GomokuGame:
    """Controller for a two-player Gomoku game."""
    def __init__(self):
        self.board = Board()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.last_move = None
        self.move_count = 0
    @property
    def current_player_name(self):
        return PLAYER_NAMES[self.current_player]
    def reset_game(self):
        """Reset the game to the initial state."""
        self.board.reset()
        self.current_player = BLACK
        self.game_over = False
        self.winner = None
        self.winning_line = None
        self.last_move = None
        self.move_count = 0
    def play_move(self, row, col):
        """Attempt to play a move for the current player.
        Returns a dict describing the outcome:
        {
            'valid': bool,
            'reason': str (if invalid),
            'win': bool,
            'draw': bool,
        }
        """
        if self.game_over:
            return {'valid': False, 'reason': 'Game is already over.'}
        if not self.board.is_empty(row, col):
            return {'valid': False, 'reason': 'Cell is occupied.'}
        self.board.place_stone(row, col, self.current_player)
        self.last_move = (row, col)
        self.move_count += 1
        result = {'valid': True, 'reason': '', 'win': False, 'draw': False}
        if self.board.check_win(row, col, self.current_player):
            self.game_over = True
            self.winner = self.current_player
            self.winning_line = self.board.get_winning_line(row, col, self.current_player)
            result['win'] = True
        elif self.board.is_full():
            self.game_over = True
            result['draw'] = True
        else:
            self.current_player = WHITE if self.current_player == BLACK else BLACK
        return result