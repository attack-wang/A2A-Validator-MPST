'''Pygame GUI: rendering, input handling and animation state machine.'''
import math
import pygame
from constants import (WINDOW_WIDTH, WINDOW_HEIGHT, BOARD_ROWS, BOARD_COLS,
                       CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT, BOARD_OFFSET_X,
                       BOARD_OFFSET_Y, FPS, CANDY_TYPES, COLOR_BACKGROUND,
                       COLOR_BOARD_LIGHT, COLOR_BOARD_DARK, COLOR_BOARD_BORDER,
                       COLOR_TEXT, COLOR_TEXT_DIM, COLOR_SELECTED, COLOR_HOVER,
                       COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_OVERLAY,
                       SWAP_DURATION, SWAP_BACK_DURATION, CLEAR_DURATION,
                       FALL_DURATION_PER_CELL, FALL_MIN_DURATION,
                       SPAWN_DROP_ROWS, STARTING_MOVES, TARGET_SCORE)
from game_engine import GameEngine
class GameGUI:
    """Pygame front-end for the match-3 game.
    Implements a small animation state machine:
    IDLE -> SWAP -> CLEAR -> FALL -> (cascade re-check) -> IDLE
    Invalid swaps play a SWAP_BACK bounce and return to IDLE.
    """
    PHASE_IDLE = "idle"
    PHASE_SWAP = "swap"
    PHASE_SWAP_BACK = "swap_back"
    PHASE_CLEAR = "clear"
    PHASE_FALL = "fall"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Candy Crush - Match 3")
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont("arial", 40, bold=True)
        self.font = pygame.font.SysFont("arial", 24, bold=True)
        self.font_small = pygame.font.SysFont("arial", 18)
        self.engine = GameEngine()
        self.phase = self.PHASE_IDLE
        self.phase_time = 0.0
        self.selected = None
        self.swap_cells = None
        self.clearing = []
        self.falling = []  # (candy, start_y, target_y, duration)
        self.restart_rect = pygame.Rect(WINDOW_WIDTH // 2 - 60, 120, 120, 36)
        self._sync_all()
    # ---------- helpers ----------
    def _cell_pixel(self, row, col):
        return (BOARD_OFFSET_X + col * CELL_SIZE,
                BOARD_OFFSET_Y + row * CELL_SIZE)
    def _cell_from_pos(self, pos):
        col = (pos[0] - BOARD_OFFSET_X) // CELL_SIZE
        row = (pos[1] - BOARD_OFFSET_Y) // CELL_SIZE
        if 0 <= row < BOARD_ROWS and 0 <= col < BOARD_COLS:
            return (int(row), int(col))
        return None
    def _sync_all(self):
        """Snap every candy's pixel position to its logical grid cell."""
        for row in self.engine.board.grid:
            for candy in row:
                if candy is not None:
                    candy.x, candy.y = self._cell_pixel(candy.row, candy.col)
                    candy.scale = 1.0
                    candy.clearing = False
    def _restart(self):
        self.engine = GameEngine()
        self.phase = self.PHASE_IDLE
        self.phase_time = 0.0
        self.selected = None
        self.swap_cells = None
        self.clearing = []
        self.falling = []
        self._sync_all()