"""Game orchestration: states, loop, HUD, difficulty progression."""
import random
import sys
import pygame
import settings
from bird import Bird
from pipemanager import PipeManager
from utils import draw_text, clamp, draw_cloud
class Game:
    """Top-level game object owning the loop, states, HUD, and difficulty."""
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont("arial", 48, bold=True)
        self.font_medium = pygame.font.SysFont("arial", 28, bold=True)
        self.font_small = pygame.font.SysFont("arial", 20)
        self.state = Game.MENU
        self.score = 0
        self.best_score = 0
        self.ground_offset = 0.0
        self.restart_lockout = 0.0
        self.background_stars = self._build_background_decor()
        self.reset_entities()
    @staticmethod
    def _build_background_decor():
        """Create deterministic decorative clouds/stars for the sky."""
        decor = []
        rng = random.Random(7)
        for _ in range(6):
            decor.append((rng.randint(40, settings.SCREEN_WIDTH - 40),
                          rng.randint(60, settings.SCREEN_HEIGHT // 2),
                          rng.uniform(0.7, 1.4)))
        return decor
    def reset_entities(self):
        """Create fresh bird/pipe objects for a new round."""
        self.bird = Bird(settings.BIRD_X_POSITION, settings.SCREEN_HEIGHT // 2)
        self.pipe_manager = PipeManager()
    def run(self):
        """Main game loop: tick, handle events, update, draw."""
        while True:
            dt = self.clock.tick(settings.FPS) / 1000.0
            dt = min(dt, 1 / 30)  # clamp to avoid tunneling after pauses
            self.handle_events()
            self.update(dt)
            self.draw()
    def handle_events(self):
        """Process quit/input events; SPACE/UP/W/click flap or restart."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    self._primary_action()
                if event.key == pygame.K_r and self.state == Game.GAME_OVER:
                    self._start_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._primary_action()
    def _primary_action(self):
        """Dispatch the primary action depending on the current state."""
        if self.state == Game.MENU:
            self._start_game()
            self.bird.flap()
        elif self.state == Game.PLAYING:
            self.bird.flap()
        elif self.state == Game.GAME_OVER:
            if self.restart_lockout <= 0.0:
                self._start_game()
    def _start_game(self):
        """Reset state and entities to begin a fresh round."""
        self.state = Game.PLAYING
        self.score = 0
        self.restart_lockout = 0.0
        self.reset_entities()
    def update(self, dt):
        """Advance the simulation for the current state."""
        if self.state == Game.MENU:
            self.bird.animate_wings(dt)
            self.ground_offset += settings.BASE_PIPE_SPEED * dt * 0.5
            return
        if self.state == Game.GAME_OVER:
            self.restart_lockout = max(0.0, self.restart_lockout - dt)
            return
        # PLAYING
        self.ground_offset += self.pipe_manager.speed * dt
        # difficulty progression: shrink gaps and speed up pipes with score
        level = min(settings.MAX_DIFFICULTY_LEVEL, self.score // settings.SCORE_PER_LEVEL)
        progress = level / settings.MAX_DIFFICULTY_LEVEL
        gap = settings.BASE_GAP_SIZE - (settings.BASE_GAP_SIZE - settings.MIN_GAP_SIZE) * progress
        speed = settings.BASE_PIPE_SPEED + (settings.MAX_PIPE_SPEED - settings.BASE_PIPE_SPEED) * progress
        self.pipe_manager.set_difficulty(gap, speed)
        # bird physics with ceiling clamp
        if self.bird.y < self.bird.radius:
            self.bird.y = self.bird.radius
            self.bird.velocity = max(self.bird.velocity, 0.0)
        self.bird.update(dt)
        self.bird.animate_wings(dt)
        # pipes
        self.pipe_manager.update(dt)
        # scoring
        for pipe in self.pipe_manager.pipes:
            if pipe.has_passed(self.bird.x):
                pipe.scored = True
                self.score += 1
        # collisions
        bird_rect = self.bird.get_rect()
        ground_y = settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT
        if self.bird.y + self.bird.radius < ground_y:
            if self.pipe_manager.collides_with(bird_rect):
                self._game_over()
        else:
            self.bird.y = ground_y - self.bird.radius
            self._game_over()
    def _game_over(self):
        """Switch to the game-over state, tracking the best score."""
        if self.score > self.best_score:
            self.best_score = self.score
        self.state = Game.GAME_OVER
        self.restart_lockout = settings.RESTART_LOCKOUT
    def draw(self):
        """Render the full frame for the current state."""
        self.screen.fill(settings.SKY_COLOR)
        for x, y, scale in self.background_stars:
            draw_cloud(self.screen, x, y, scale, (230, 245, 250))
        self.pipe_manager.draw(self.screen)
        self._draw_ground(self.screen)
        self.bird.draw(self.screen)
        if self.state == Game.MENU:
            draw_text(self.screen, settings.TITLE, self.font_big, settings.TEXT_COLOR,
                      (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3),
                      settings.TEXT_SHADOW_COLOR)
            draw_text(self.screen, "Press SPACE to flap", self.font_medium, settings.TEXT_COLOR,
                      (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2),
                      settings.TEXT_SHADOW_COLOR)
            draw_text(self.screen, f"Best: {self.best_score}", self.font_small, settings.TEXT_COLOR,
                      (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 40),
                      settings.TEXT_SHADOW_COLOR)
        elif self.state == Game.PLAYING:
            draw_text(self.screen, str(self.score), self.font_big, settings.SCORE_COLOR,
                      (settings.SCREEN_WIDTH // 2, 60), settings.TEXT_SHADOW_COLOR)
        else:
            self._draw_game_over()
        pygame.display.flip()
    def _draw_ground(self, surface):
        """Draw the scrolling ground band with diagonal stripes."""
        ground_rect = pygame.Rect(0, settings.SCREEN_HEIGHT - settings.GROUND_HEIGHT,
                                  settings.SCREEN_WIDTH, settings.GROUND_HEIGHT)
        pygame.draw.rect(surface, settings.GROUND_COLOR, ground_rect)
        pygame.draw.rect(surface, settings.GROUND_LINE_COLOR,
                         (0, ground_rect.y, settings.SCREEN_WIDTH, 4))
        stripe_w = 24
        offset = int(self.ground_offset) % stripe_w
        for x in range(-stripe_w, settings.SCREEN_WIDTH + stripe_w, stripe_w):
            pygame.draw.polygon(surface, settings.GROUND_STRIPE_COLOR,
                                [(x + offset, ground_rect.y + 4),
                                 (x + offset + stripe_w // 2, ground_rect.y + 4),
                                 (x + offset, ground_rect.bottom)])
    def _draw_game_over(self):
        """Draw the game-over overlay with final and best scores."""
        draw_text(self.screen, "GAME OVER", self.font_big, settings.TEXT_COLOR,
                  (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3),
                  settings.TEXT_SHADOW_COLOR)
        draw_text(self.screen, f"Score: {self.score}", self.font_medium, settings.TEXT_COLOR,
                  (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2),
                  settings.TEXT_SHADOW_COLOR)
        draw_text(self.screen, f"Best: {self.best_score}", self.font_medium, settings.TEXT_COLOR,
                  (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 40),
                  settings.TEXT_SHADOW_COLOR)
        draw_text(self.screen, "Press SPACE or R to restart", self.font_small, settings.TEXT_COLOR,
                  (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 90),
                  settings.TEXT_SHADOW_COLOR)