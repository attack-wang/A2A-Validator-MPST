'''
game.py
Game class: interactive two-player checkers game loop, input parsing,
turn management, forced captures, multi-jumps, win/draw detection.
'''
import re
from board import Board
from piece import Piece
from exceptions import NotationError, IllegalMoveError
class Game:
    MAX_IDLE_MOVES = 80  # draw if 80 consecutive moves (40 per player) with no capture and no man move
    def __init__(self):
        self.board = Board()
        self.current_color = Piece.BLACK  # black moves first (standard draughts rule)
        self.mandatory_piece = None  # (row, col) when a multi-jump must continue
        self.idle_moves = 0
        self.game_over = False
        self.winner = None  # None, Piece.RED, Piece.BLACK, or 'draw'
    def run(self):
        self.print_intro()
        while not self.game_over:
            self.print_board()
            self.prompt_move()
        self.print_result()