"""Entry point: game loop, input handling, timer, and win/lose logic."""
import math
import random
import sys
import pygame
import settings
from claw import Claw
from floatingtext import FloatingText
from level import Level
from objects import Explosion
class Game:
    """Top-level game object: owns the window, states, and main loop."""
    PLAYING = "playing"
    LEVEL_CLEAR = "level_clear"
    GAME_OVER = "game_over"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 56)
        self.small_font = pygame.font.SysFont(None, 22)
        self.score = 0
        self.level_number = 1
        self.start_level()
    def start_level(self):
        self.level = Level(self.level_number)
        self.time_left = float(self.level.time_limit)
        self.claw = Claw()
        self.explosions = []
        self.texts = []
        self.state = self.PLAYING
    def run(self):
        while True:
            dt = self.clock.tick(settings.FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
            pygame.display.flip()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == self.PLAYING:
                        self.claw.launch()
                    elif self.state == self.LEVEL_CLEAR:
                        self.level_number += 1
                        self.start_level()
                    elif self.state == self.GAME_OVER:
                        self.score = 0
                        self.level_number = 1
                        self.start_level()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    def update(self, dt):
        if self.state != self.PLAYING:
            return
        self.time_left = max(0.0, self.time_left - dt)
        for name, obj in self.claw.update(dt, self.level.objects):
            if name == "grab":
                if obj.kind == "mystery":
                    obj.value = random.choice([50, 100, 200, 400, 750])
                self.texts.append(FloatingText(obj.x, obj.y - 20, f"{obj.weight:.1f}kg", settings.COLOR_WHITE))
            elif name == "deposit":
                self.score += obj.value
                color = settings.COLOR_GREEN if obj.value > 0 else settings.COLOR_RED
                self.texts.append(FloatingText(settings.CLAW_PIVOT_X, settings.GROUND_Y - 20,
                                               f"+${obj.value}", color))
            elif name == "explode":
                self.explosions.append(Explosion(obj.x, obj.y))
                for other in self.level.objects:
                    if other.alive and math.hypot(other.x - obj.x, other.y - obj.y) <= settings.TNT_BLAST_RADIUS + other.radius:
                        other.alive = False
                        self.texts.append(FloatingText(other.x, other.y - 10, "destroyed", settings.COLOR_RED))
        for ex in self.explosions:
            ex.update(dt)
        self.explosions = [e for e in self.explosions if not e.done]
        for t in self.texts:
            t.update(dt)
        self.texts = [t for t in self.texts if not t.expired]
        # Level end conditions
        if self.score >= self.level.target:
            bonus = int(self.time_left * settings.TIME_BONUS_PER_SECOND)
            self.score += bonus
            self.time_bonus = bonus
            self.state = self.LEVEL_CLEAR
        elif self.time_left <= 0:
            self.state = self.GAME_OVER