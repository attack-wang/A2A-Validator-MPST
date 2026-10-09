'''
Game module: contains the main Game class managing states, difficulty, rendering.
'''
import random
import sys
import pygame
from settings import *
from bird import Bird
from pipe import Pipe
from audio import Audio
from utils import (load_high_score, save_high_score, make_gradient_surface,
                   draw_cloud, draw_ground)
class Game:
    """Manages game states, entities, difficulty scaling and rendering."""
    MENU, PLAYING, GAME_OVER = 0, 1, 2
    def __init__(self):
        self.audio = Audio()          # set up mixer before pygame.init()
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird - ChatDev Edition")
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.Font(None, 64)
        self.font_med = pygame.font.Font(None, 44)
        self.font_small = pygame.font.Font(None, 30)
        self.high_score = load_high_score()
        self.sky = make_gradient_surface(SCREEN_WIDTH,
                                         SCREEN_HEIGHT - GROUND_HEIGHT,
                                         SKY_TOP, SKY_BOTTOM)
        # Decorative clouds: [x, y, scale, drift_speed]
        self.clouds = [[random.randint(0, SCREEN_WIDTH),
                        random.randint(40, 260),
                        random.uniform(0.7, 1.4),
                        random.uniform(0.1, 0.4)] for _ in range(5)]
        self.ground_scroll = 0
        self.state = self.MENU
        self.reset()
    def reset(self):
        """Reset all per-round state (must init distance_since_spawn)."""
        self.bird = Bird(BIRD_X, SCREEN_HEIGHT // 2 - 50)
        self.pipes = []
        self.score = 0
        self.distance_since_spawn = PIPE_SPACING  # spawn 1st pipe immediately
        self.death_flash = 0
        self.game_over_timer = 0                  # prevents instant restart
    # ---------------- Difficulty scaling ----------------
    def current_speed(self):
        """Pipe scroll speed, capped at MAX_SPEED."""
        return min(MAX_SPEED, BASE_SPEED + self.score * SPEED_INCREASE_PER_POINT)
    def current_gap(self):
        """Gap height shrinks with score, plus random GAP_VARIATION."""
        base = max(MIN_GAP, BASE_GAP - self.score * GAP_SHRINK_PER_POINT)
        return base + random.randint(-GAP_VARIATION, GAP_VARIATION)
    def spawn_pipe(self):
        """Spawn a pipe, clamping the gap center inside safe margins."""
        gap = self.current_gap()
        half = gap // 2
        lo = GAP_MARGIN_TOP + half
        hi = SCREEN_HEIGHT - GROUND_HEIGHT - GAP_MARGIN_BOTTOM - half
        gap_center = random.randint(lo, max(lo, hi))
        self.pipes.append(Pipe(SCREEN_WIDTH + PIPE_WIDTH, gap_center, gap))
    # ---------------- Core loop pieces ----------------
    def handle_keydown(self, key):
        """Dispatch key presses per game state (flap / start / restart)."""
        if key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        if key in (pygame.K_SPACE, pygame.K_UP):
            if self.state == self.MENU:
                self.state = self.PLAYING
                self.bird.flap()
                self.audio.play('flap')
            elif self.state == self.PLAYING:
                self.bird.flap()
                self.audio.play('flap')
            elif self.state == self.GAME_OVER and self.game_over_timer <= 0:
                self.reset()
                self.state = self.PLAYING
    def game_over(self):
        """Handle death: flash, sound, persist high score."""
        self.state = self.GAME_OVER
        self.death_flash = 10
        self.game_over_timer = 30
        self.audio.play('hit')
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)
    def update(self):
        """Advance world simulation one frame."""
        for c in self.clouds:                       # ambient cloud drift (all states)
            c[0] -= c[3]
            if c[0] < -60:
                c[0] = SCREEN_WIDTH + 60
        if self.state == self.PLAYING:
            speed = self.current_speed()
            self.ground_scroll = (self.ground_scroll + speed) % 48
            self.bird.update()
            ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
            if self.bird.y + self.bird.radius >= ground_y:   # ground collision
                self.bird.y = ground_y - self.bird.radius
                self.game_over()
                return
            self.distance_since_spawn += speed
            if self.distance_since_spawn >= PIPE_SPACING:    # spawn pipes
                self.spawn_pipe()
                self.distance_since_spawn = 0
            bird_rect = self.bird.rect
            for pipe in self.pipes:
                pipe.update(speed)
                if pipe.collides(bird_rect):                 # pipe collision
                    self.game_over()
                    return
                if pipe.has_passed(self.bird.x):             # scoring
                    pipe.scored = True
                    self.score += 1
                    self.audio.play('score')
            self.pipes = [p for p in self.pipes if not p.offscreen()]
        elif self.state == self.GAME_OVER:
            if self.death_flash > 0:
                self.death_flash -= 1
            if self.game_over_timer > 0:
                self.game_over_timer -= 1
    def draw(self):
        """Render sky, clouds, pipes, ground, bird, HUD and overlays."""
        self.screen.blit(self.sky, (0, 0))
        for x, y, scale, _ in self.clouds:
            draw_cloud(self.screen, x, y, scale)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        draw_ground(self.screen, self.ground_scroll)
        self.bird.draw(self.screen)
        score_txt = self.font_big.render(str(self.score), True, WHITE)
        self.screen.blit(score_txt, score_txt.get_rect(center=(SCREEN_WIDTH // 2, 60)))
        if self.state == self.MENU:
            self._center_text("FLAPPY BIRD", self.font_med, SCREEN_HEIGHT // 2 - 80)
            self._center_text("Press SPACE to flap", self.font_small, SCREEN_HEIGHT // 2 - 30)
            self._center_text(f"Best: {self.high_score}", self.font_small, SCREEN_HEIGHT // 2 + 10)
        elif self.state == self.GAME_OVER:
            self._center_text("GAME OVER", self.font_med, SCREEN_HEIGHT // 2 - 60)
            self._center_text(f"Score: {self.score}  Best: {self.high_score}",
                              self.font_small, SCREEN_HEIGHT // 2 - 10)
            if self.game_over_timer <= 0:
                self._center_text("Press SPACE to retry", self.font_small,
                                  SCREEN_HEIGHT // 2 + 40)
        if self.death_flash > 0:                        # white death flash
            flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash.fill(WHITE)
            flash.set_alpha(self.death_flash * 25)
            self.screen.blit(flash, (0, 0))
        pygame.display.flip()
    def _center_text(self, text, font, y):
        """Helper: blit a centered text line."""
        surf = font.render(text, True, BLACK)
        self.screen.blit(surf, surf.get_rect(center=(SCREEN_WIDTH // 2, y)))
    def run(self):
        """Main loop: events -> update -> draw at FPS."""
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event.key)
            self.update()
            self.draw()
        pygame.quit()