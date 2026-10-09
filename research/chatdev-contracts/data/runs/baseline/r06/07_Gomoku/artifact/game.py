'''
game.py
Game-flow module for the Gomoku game. Provides the GameController class,
which owns the Board and GUI, manages turn alternation between the black
and white players, applies moves, detects wins and draws, updates the
status message, and supports restarting the game.
'''
from board import Board
from gui import GUI
from constants import (
    BLACK, WHITE,
    MSG_BLACK_TURN, MSG_WHITE_TURN,
    MSG_BLACK_WIN, MSG_WHITE_WIN, MSG_DRAW,
    MSG_RESTART_HINT,
)
class GameController:
    '''Coordinates board state, rendering, and the rules of Gomoku.'''
    def __init__(self, screen):
        '''Create the board, the GUI renderer, and set up a fresh game.'''
        self.board = Board()
        self.gui = GUI(screen)
        self.current_player = BLACK  # Black always moves first
        self.game_over = False
        self.win_cells = None        # Cells of the winning line, if any
        self.status_text = MSG_BLACK_TURN
    def reset(self):
        '''Start a new game: clear the board and give Black the first move.'''
        self.board.reset()
        self.current_player = BLACK
        self.game_over = False
        self.win_cells = None
        self.status_text = MSG_BLACK_TURN
    def handle_click(self, row, col):
        '''
        Process a click on board intersection (row, col).
        Ignores the click when the game is over or the move is invalid.
        Otherwise places the stone, checks for a win or a draw, and either
        ends the game or hands the turn to the other player.
        '''
        if self.game_over:
            return
        if not self.board.place_stone(row, col, self.current_player):
            return  # Invalid move (occupied or out of bounds): ignore.
        self.win_cells = self.board.check_win(row, col, self.current_player)
        if self.win_cells:
            self.game_over = True
            self.status_text = (MSG_BLACK_WIN if self.current_player == BLACK
                                else MSG_WHITE_WIN)
        elif self.board.is_full():
            self.game_over = True
            self.status_text = MSG_DRAW
        else:
            self.switch_turn()
    def switch_turn(self):
        '''Alternate between black and white and refresh the status text.'''
        self.current_player = WHITE if self.current_player == BLACK else BLACK
        self.status_text = (MSG_BLACK_TURN if self.current_player == BLACK
                            else MSG_WHITE_TURN)
    def update_display(self, hover_cell=None):
        '''
        Render the current state. When the game is over, append the restart
        hint and suppress the hover preview.
        '''
        display_text = self.status_text
        if self.game_over:
            display_text = f"{self.status_text}  |  {MSG_RESTART_HINT}"
            hover_cell = None
        self.gui.draw(self.board, display_text, self.win_cells,
                      hover_cell, self.current_player)