'''Game controller: state machine, input handling, scoring, modes and top-level update logic.'''
import random
import pygame
import config
from board import Board
from effects import Popup, Particle, Animation, get_font
from sound import SoundManager
STATE_MENU = 'menu'
STATE_IDLE = 'idle'
STATE_SWAPPING = 'swapping'
STATE_SWAP_BACK = 'swap_back'
STATE_CLEARING = 'clearing'
STATE_FALLING = 'falling'
STATE_GAME_OVER = 'game_over'
class Game:
    def __init__(self):
        self.board = Board(config.GRID_SIZE, config.GRID_SIZE, config.NUM_CANDY_TYPES)
        self.sound = SoundManager()
        self.score = 0
        self.moves = config.INITIAL_MOVES
        self.time_left = config.TIME_LIMIT_SECONDS
        self.cascade = 0
        self.state = STATE_MENU
        self.selected = None          # (r, c) selected cell
        self.swap_candidate = None    # (r, c) the cell to swap with
        self.pending_swap = None      # ((r1,c1),(r2,c2)) currently animating
        self.hint_cells = None
        self.hint_timer = 0.0
        self.popups = []
        self.particles = []
        self.banner = None            # Animation for "shuffling" etc.
        self.game_over_win = False
        self.board_offset = config.BOARD_TOP_LEFT
        self.shake = 0.0  # optional screen shake on big matches? maybe skip