"""Game orchestration: states, loop, input, difficulty, rendering."""
import os
import math
import random
import sys
import pygame
import settings as cfg
from bird import Bird
from pipe import PipeManager
from utils import draw_text, load_high_score, save_high_score, clamp
from sounds import SoundManager
STATE_START = "start"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
class Game:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 2, 512)
        pygame.init()
        self.screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
        pygame.display.set_caption(cfg.TITLE)
        self.clock = pygame.time.Clock()
        self.sounds = SoundManager()
        self.high_score_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")
        self.high_score = load_high_score(self.high_score_path)
        self.background = self._build_background()
        self.ground_offset = 0.0
        self.font = ...  # via utils
        self.reset()
        self.state = STATE_START