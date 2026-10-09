'''
Core game orchestration: states, input, physics updates, collisions, scoring.
'''
import math
import random
import pygame
import settings
from bird import Bird
from pipe import Pipe
from background import Background
from ui import HUD, draw_text
from screens import Screens
STATE_START = "start"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
FLASH_DURATION = 0.25
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird - ChatDev")
        self.clock = pygame.time.Clock()
        self.hud = HUD()
        self.background = Background()
        self.best_score = self._load_best_score()
        self.running = False
        self.reset()
        self.state = STATE_START
    def reset(self):
        """Reset the playfield for a fresh run."""
        self.bird = Bird(settings.BIRD_X, settings.SCREEN_HEIGHT * 0.4)
        self.pipes = []
        self.score = 0
        self.distance_since_spawn = 0.0
        self.flash_timer = 0.0
        self.idle_timer = 0.0
        self.idle_base_y = self.bird.y
        self.game_over_timer = 0.6
    # difficulty
    def _difficulty_progress(self):
        return min(1.0, self.score / float(settings.DIFFICULTY_SCORE_SPAN))
    def _current_pipe_speed(self):
        p = self._difficulty_progress()
        return settings.BASE_PIPE_SPEED + (settings.MAX_PIPE_SPEED - settings.BASE_PIPE_SPEED) * p
    def _current_gap_size(self):
        p = self._difficulty_progress()
        base = settings.BASE_GAP_SIZE + (settings.MIN_GAP_SIZE - settings.BASE_GAP_SIZE) * p
        return max(settings.MIN_GAP_SIZE, base + random.uniform(-settings.GAP_VARIANCE, settings.GAP_VARIANCE))
    def _spawn_pipe_if_needed(self, dt):
        speed = self._current_pipe_speed()
        self.distance_since_spawn += speed * dt
        if self.distance_since_spawn >= settings.PIPE_SPAWN_DISTANCE or not self.pipes:
            self.distance_since_spawn = 0.0
            gap_size = self._current_gap_size()
            ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
            margin = settings.PIPE_SPAWN_MARGIN
            lo = gap_size / 2.0 + margin
            hi = ground_top - gap_size / 2.0 - margin
            gap_center = random.uniform(lo, hi)
            self.pipes.append(Pipe(settings.SCREEN_WIDTH + settings.PIPE_WIDTH, gap_center, gap_size, speed))
    def update(self, dt):
        if self.state == STATE_START:
            self.idle_timer += dt
            self.bird.y = self.idle_base_y + math.sin(self.idle_timer * 3.0) * 8.0
            self.bird.wing_timer += dt * 10.0
            self.background.update(dt, settings.BASE_PIPE_SPEED * 0.4)
        elif self.state == STATE_PLAYING:
            speed = self._current_pipe_speed()
            self.background.update(dt, speed)
            self.bird.update(dt)
            # Ceiling clamp
            if self.bird.y < settings.BIRD_RADIUS:
                self.bird.y = settings.BIRD_RADIUS
                self.bird.velocity = max(self.bird.velocity, 0.0)
            self._spawn_pipe_if_needed(dt)
            for pipe in self.pipes:
                pipe.speed = speed
                pipe.update(dt)
            # Scoring
            for pipe in self.pipes:
                if pipe.has_passed(self.bird.x):
                    pipe.mark_scored()
                    self.score += 1
            # Remove offscreen pipes
            self.pipes = [p for p in self.pipes if not p.offscreen()]
            # Collisions
            bird_rect = self.bird.rect
            ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
            hit_pipe = any(pipe.collides(bird_rect) for pipe in self.pipes)
            hit_ground = self.bird.y + settings.BIRD_RADIUS >= ground_top
            if hit_pipe or hit_ground:
                self.bird.alive = False
                self.state = STATE_GAME_OVER
                self.flash_timer = FLASH_DURATION
                if self.score > self.best_score:
                    self.best_score = self.score
                    self._save_best_score()
        else:  # STATE_GAME_OVER
            self.game_over_timer -= dt
            ground_top = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
            if self.bird.y + settings.BIRD_RADIUS < ground_top:
                self.bird.update(dt)
            else:
                self.bird.y = ground_top - settings.BIRD_RADIUS
                self.bird.velocity = 0.0
            if self.flash_timer > 0:
                self.flash_timer = max(0.0, self.flash_timer - dt)
    def draw(self):
        self.background.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.bird.draw(self.screen)
        if self.state == STATE_PLAYING:
            self.hud.draw_score(self.screen, self.score)
            level = 1 + int(self._difficulty_progress() * 9)
            self.hud.draw_difficulty(self.screen, level)
        elif self.state == STATE_START:
            Screens.draw_start(self.screen)
        else:
            Screens.draw_game_over(self.screen, self.score, self.best_score)
        if self.flash_timer > 0:
            flash = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            flash.fill((255, 255, 255))
            flash.set_alpha(int(120 * (self.flash_timer / FLASH_DURATION)))
            self.screen.blit(flash, (0, 0))
        pygame.display.flip()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    self._flap_action()
                elif event.key == pygame.K_r and self.state == STATE_GAME_OVER and self.game_over_timer <= 0:
                    self.reset()
                    self.state = STATE_START
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._flap_action()
    def _flap_action(self):
        if self.state == STATE_START:
            self.state = STATE_PLAYING
            self.bird.flap()
        elif self.state == STATE_PLAYING:
            self.bird.flap()
        elif self.state == STATE_GAME_OVER:
            # small delay before restart allowed to avoid accidental instant restart
            if self.game_over_timer <= 0:
                self.reset()
                self.state = STATE_START
    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000.0
            dt = min(dt, 1.0 / 30.0)  # clamp to avoid tunneling after stalls
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
    def _load_best_score(self):
        """Load the persisted best score, tolerating missing/corrupt files."""
        try:
            with open(settings.BEST_SCORE_FILE, "r") as f:
                return int(f.read().strip() or 0)
        except (IOError, OSError, ValueError):
            return 0
    def _save_best_score(self):
        """Persist the best score; failures are silently ignored."""
        try:
            with open(settings.BEST_SCORE_FILE, "w") as f:
                f.write(str(self.best_score))
        except (IOError, OSError):
            pass