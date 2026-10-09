"""Main Game class: state machine, event handling, update and render loop."""
import math
import random
import sys
import pygame
from settings import *
from objects import Gold, Rock, Diamond, TNT, Bone, MysteryBag
from claw import Claw
from level import level_config, generate_objects
from ui import HUD, FloatingText
MENU, PLAYING, LEVEL_COMPLETE, GAME_OVER = "menu", "playing", "level_complete", "game_over"
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.hud = HUD()
        self.state = MENU
        self.level_num = 1
        self.total_score = 0
        self.floating = []
        self.shake = 0.0
        self.speckles = self._make_speckles()
        self._start_level(1)
        self.state = MENU  # start at menu after preloading level 1