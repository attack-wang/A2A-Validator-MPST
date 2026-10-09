'''Game: main game class with state machine, input handling, rendering, HUD.'''
import math
import random
import pygame
from constants import *
from board import Board
from candy import Candy
from ui import draw_hud, draw_game_over, ...
class Game:
    STATE_IDLE = 'idle'
    STATE_SWAPPING = 'swapping'
    STATE_SWAP_BACK = 'swap_back'
    STATE_CLEARING = 'clearing'
    STATE_FALLING = 'falling'
    STATE_GAME_OVER = 'game_over'
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Candy Match")
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont(None, 48)  # or Font
        ...
        self.reset_game()
    def reset_game(self):
        self.board = Board()
        self.score = 0
        self.moves_left = INITIAL_MOVES
        self.combo = 0
        self.state = STATE_IDLE
        self.selected = None  # (r, c)
        self.swap_anim = None  # dict with candies, positions, progress
        self.clearing = None  # set of positions with progress
        self.falling = False
        ...
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
    def handle_events(self): ...
    def on_click(self, pos): ...
    def update(self, dt): ...
    def draw(self): ...