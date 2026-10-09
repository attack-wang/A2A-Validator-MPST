'''
minesweepergui.py
The main application class for the Minesweeper game.
Owns the pygame window, the game loop and all event handling, and ties
together the Board model (board.py) with the reusable widgets (gui.py).
Modes:
    * MODE_MENU - difficulty selection screen (beginner/intermediate/expert)
    * MODE_GAME - the playing field with header, timer, mine counter,
                  smiley reset button and the cell grid.
Controls:
    * Left click  - uncover a cell
    * Right click - toggle a flag on a suspected mine
    * Smiley / R  - restart the current difficulty
    * Escape      - back to the main menu
'''
import math
import time
import pygame
from board import Board
from gui import Button, SmileyButton
from config import (CELL_SIZE, BOARD_MARGIN, HEADER_HEIGHT,
                    MENU_WIDTH, MENU_HEIGHT,
                    DIFFICULTIES, DIFFICULTY_ORDER,
                    FONT_NAME, FONT_TITLE_SIZE, FONT_UI_SIZE,
                    FONT_COUNTER_SIZE, FONT_NUMBER_SIZE, FONT_OVERLAY_SIZE,
                    COLOR_BACKGROUND, COLOR_PANEL, COLOR_PANEL_DARK,
                    COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_BUTTON_TEXT,
                    COLOR_BEVEL_DARK, COLOR_BEVEL_LIGHT,
                    COLOR_CELL_HIDDEN, COLOR_CELL_HIDDEN_EDGE,
                    COLOR_CELL_REVEALED, COLOR_CELL_REVEALED_EDGE,
                    COLOR_CELL_EXPLODED, COLOR_MINE, COLOR_MINE_WRONG,
                    COLOR_NUMBERS, COLOR_FLAG_POLE, COLOR_FLAG_CLOTH,
                    COLOR_COUNTER_BG, COLOR_COUNTER_TEXT,
                    COLOR_OVERLAY_WIN, COLOR_OVERLAY_LOSE, COLOR_OVERLAY_TEXT)
class MinesweeperGUI:
    """Top-level pygame application: menu, game screen and event routing."""
    MODE_MENU = "menu"
    MODE_GAME = "game"
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.mode = self.MODE_MENU
        self.running = True
        self.difficulty_name = None
        self.board = None
        self.cell_size = CELL_SIZE
        self.board_origin = (BOARD_MARGIN, HEADER_HEIGHT + BOARD_MARGIN)
        self.window_size = (MENU_WIDTH, MENU_HEIGHT)
        self.menu_buttons = []
        self._build_menu()
        self.reset_button_rect = None
        self.smiley = None
        self.start_time = None
        self.elapsed_time = 0
        self.final_time = None
        self._make_fonts()
        self.screen = pygame.display.set_mode(self.window_size)
        self.mouse_pos = (0, 0)
        self.mouse_pressed = False  # left button held on a cell (peek effect)
        self.peek_cell = None