'''
game.py
Core game loop, level generation and state management for Gold Miner.
'''
import math
import random
import sys
import pygame
import config
from claw import Claw
from objects import (GameObject, Gold, Diamond, Rock, Skull, MysteryBag, TNT)
from ui import draw_hud, draw_message, draw_text
class GoldMinerGame:
    """Main application: owns the window, the loop and the game state."""
    STATE_PLAYING = "playing"
    STATE_LEVEL_COMPLETE = "level_complete"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Gold Miner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 22, bold=True)
        self.big_font = pygame.font.SysFont("arial", 40, bold=True)
        self.small_font = pygame.font.SysFont("arial", 16)
        self.level = 1
        self.score = 0
        self.reset(full=True)
    def reset(self, full=False):
        """Reset the running state; full reset also clears score/level."""
        if full:
            self.level = 1
            self.score = 0
        self.state = self.STATE_PLAYING
        self.time_left = self._level_time(self.level)
        self.target = self._level_target(self.level)
        self.claw = Claw()
        self.claw.set_swing_speed(self._swing_speed(self.level))
        self.objects = self._generate_level(self.level)
        self.message = ""
        self.flash_timer = 0.0
        self.last_grab_info = None
        self.explosions = []
        self.speckles = self._make_speckles()