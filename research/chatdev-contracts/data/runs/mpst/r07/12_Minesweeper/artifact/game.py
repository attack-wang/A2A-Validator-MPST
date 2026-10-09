'''
game.py
Controller gluing the board model and GUI together; manages game state,
the turn flow (reveal / flag / chord) and the elapsed-time timer.
'''
import tkinter as tk
from tkinter import messagebox
from board import Board
from gui import MinesweeperGUI
from config import (DIFFICULTIES, DEFAULT_DIFFICULTY, STATE_READY, STATE_PLAYING, STATE_WON, STATE_LOST, FACE_PLAYING, FACE_WON, FACE_LOST)
class Game:
    def __init__(self, master):
        self.master = master
        self.state = STATE_READY
        self.elapsed = 0
        self._timer_job = None
        self.difficulty_name = DEFAULT_DIFFICULTY
        self.board = self._make_board(self.difficulty_name)
        self.gui = MinesweeperGUI(master, self)
        self.gui.new_round()
    def _make_board(self, difficulty_name):
        preset = DIFFICULTIES[difficulty_name]
        return Board(preset["rows"], preset["cols"], preset["mines"])
    def start_new_game(self, difficulty_name):
        self._stop_timer()
        self.difficulty_name = difficulty_name
        self.state = STATE_READY
        self.elapsed = 0
        self.board = self._make_board(difficulty_name)
        self.gui.new_round()
    def restart(self):
        self.start_new_game(self.difficulty_name)
    # -- input handlers ------------------------------------------------
    def handle_reveal(self, row, col):
        if self.state not in (STATE_READY, STATE_PLAYING):
            return
        cell = self.board.get_cell(row, col)
        if cell.is_flagged:
            return
        if cell.is_revealed:
            self.handle_chord(row, col)
            return
        revealed_cells = self.board.reveal_cell(row, col)
        if any(c.is_mine for c in revealed_cells):
            self._lose(row, col)
            return
        if self.state == STATE_READY:
            self.state = STATE_PLAYING
            self._start_timer()
        if self.board.check_win():
            self._win()
            return
        self.gui.redraw_board()
        self.gui.update_mine_counter(self.board.num_mines - self.board.count_flagged())
    def handle_flag(self, row, col):
        if self.state not in (STATE_READY, STATE_PLAYING):
            return
        if self.board.toggle_flag(row, col):
            self.gui.redraw_board()
            self.gui.update_mine_counter(self.board.num_mines - self.board.count_flagged())
    def handle_chord(self, row, col):
        if self.state not in (STATE_READY, STATE_PLAYING):
            return
        cell = self.board.get_cell(row, col)
        if not cell.is_revealed or cell.adjacent_mines == 0:
            return
        neighbors = self.board.get_neighbors(row, col)
        flagged = sum(1 for r, c in neighbors if self.board.get_cell(r, c).is_flagged)
        if flagged != cell.adjacent_mines:
            return
        hit_mine = None
        for r, c in neighbors:
            n = self.board.get_cell(r, c)
            if n.is_flagged or n.is_revealed:
                continue
            revealed = self.board.reveal_cell(r, c)
            if any(x.is_mine for x in revealed):
                hit_mine = (r, c)
                break
        if hit_mine is not None:
            self._lose(hit_mine[0], hit_mine[1])
            return
        if self.board.check_win():
            self._win()
            return
        self.gui.redraw_board()
        self.gui.update_mine_counter(self.board.num_mines - self.board.count_flagged())