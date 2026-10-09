'''
main.py
Entry point and game loop for the match-3 puzzle game: input handling,
animation state machine, HUD rendering and win/lose flow.
'''
import sys
import pygame
import config
from board import Board
from sounds import Sounds
class Game:
    """Drives the full game: input, animations, scoring and rendering."""
    STATE_PLAYING = "playing"
    STATE_WIN = "win"
    STATE_LOSE = "lose"
    PHASE_IDLE = "idle"
    PHASE_SWAP = "swap"
    PHASE_SWAP_BACK = "swap_back"
    PHASE_CLEAR = "clear"
    PHASE_FALL = "fall"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption("Candy Match — Match-3 Puzzle")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(config.FONT_NAME, 34)
        self.font_medium = pygame.font.Font(config.FONT_NAME, 24)
        self.font_small = pygame.font.Font(config.FONT_NAME, 18)
        self.sounds = Sounds()
        self.reset()
    def reset(self):
        """Start a fresh game."""
        self.board = Board()
        self.score = 0
        self.moves_left = config.MAX_MOVES
        self.time_left = float(config.GAME_TIME_LIMIT)
        self.state = self.STATE_PLAYING
        self.phase = self.PHASE_IDLE
        self.selected = None            # (row, col) currently selected
        self.hint = None                # ((r1,c1),(r2,c2)) hinted swap
        self.hint_timer = 0.0
        self.popups = []                # floating score texts
        # swap animation data
        self.swap_pair = None           # (candy_a, candy_b)
        self.swap_t = 0.0
        self.swap_valid = False
        # clear animation data
        self.clearing = []              # candies currently fading out
        self.clear_t = 0.0
        self.combo = 0                  # current chain-reaction depth
        self.pending_matches = set()    # cells being cleared this step