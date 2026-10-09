'''
game.py
Game controller module containing the GomokuGame class.
This class manages the flow of a Gomoku match on top of the Board:
whose turn it is, applying moves, detecting wins/draws, keeping a
move history for undo, and resetting the game. It is completely
independent from the GUI layer.
'''
from board import Board
from config import EMPTY, PLAYER_BLACK, PLAYER_WHITE
class GomokuGame:
    """Controller that manages the state and flow of a Gomoku game."""
    def __init__(self, board_size=15):
        self.board = Board(board_size)
        self.current_player = PLAYER_BLACK   # Black always moves first
        self.game_over = False
        self.winner = None                   # PLAYER_BLACK/WHITE or None (draw)
        self.winning_line = []               # Cells forming the winning five
        self.move_history = []               # List of (row, col, player)
    @property
    def board_size(self):
        return self.board.size
    def make_move(self, row, col):
        """
        Attempt to place a stone for the current player at (row, col).
        Returns True if the move was applied. Handles turn switching,
        win detection and draw detection.
        """
        if self.game_over:
            return False
        if not self.board.place_stone(row, col, self.current_player):
            return False
        self.move_history.append((row, col, self.current_player))
        winning = self.board.check_win(row, col, self.current_player)
        if winning:
            self.game_over = True
            self.winner = self.current_player
            self.winning_line = winning
        elif self.board.is_full():
            self.game_over = True
            self.winner = None  # Draw
        else:
            # Switch turns
            self.current_player = (PLAYER_WHITE if self.current_player == PLAYER_BLACK
                                   else PLAYER_BLACK)
        return True
    def undo_move(self):
        """
        Undo the last move (if any) and restore the turn order.
        Returns True if a move was undone.
        """
        if not self.move_history:
            return False
        row, col, player = self.move_history.pop()
        self.board.grid[row][col] = EMPTY
        self.game_over = False
        self.winner = None
        self.winning_line = []
        self.current_player = player  # It is again that player's turn
        return True
    def reset(self):
        """Start a fresh game."""
        self.board.reset()
        self.current_player = PLAYER_BLACK
        self.game_over = False
        self.winner = None
        self.winning_line = []
        self.move_history = []
    def get_current_player(self):
        return self.current_player
    def is_game_over(self):
        return self.game_over
    def get_winner(self):
        return self.winner
    def get_winning_line(self):
        return self.winning_line
    def get_move_count(self):
        return len(self.move_history)